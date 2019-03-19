import requests
import json
from flask import Flask, request
from concurrent.futures import ThreadPoolExecutor
from wunderlist import WunderApi
from trello import TrelloApi
from functools import lru_cache
import dateutil.parser
import datetime


app = Flask(__name__)
executor = ThreadPoolExecutor(1)

wunderlist = WunderApi(
  os.environ['WUNDERLIST_ACCESS_TOKEN'],
  os.environ['WUNDERLIST_CLIENT_ID']
)

trello = TrelloApi(
  os.environ['TRELLO_ACCESS_TOKEN'],
  os.environ['TRELLO_CLIENT_ID']
)


@app.route('/trello', methods=['HEAD', 'POST'])
def trello_hook():
  if request.method == 'HEAD': return ('', 200)

  data = request.json
  executor.submit(process_trello_hook, data)
  return ('', 200)


@app.route('/wunderlist', methods=['POST'])
def wunderlist_hook():
  data = request.json
  executor.submit(process_wunderlist_hook, data)
  return ('', 200)


def process_trello_hook(data):
  action = data.get('action', {}).get('display', {}).get('translationKey')
  if action == 'action_move_card_from_list_to_list':
    process_trello_moved_card(data)
  elif action == 'action_renamed_card':
    process_trello_renamed_card(data)
  elif action == 'action_create_card':
    process_trello_created_card(data)
  elif action == 'action_archived_card':
    process_trello_archived_card(data)


def process_trello_moved_card(data):
  entities = data['action']['display']['entities']
  card = entities['card']['text']
  list_before = entities['listBefore']['text']
  list_after = entities['listAfter']['text']

  if list_after == 'Done':
    process_trello_completed_card(card)


def process_trello_completed_card(card):
  task = find_wunderlist_task(card)
  if not task: return
  wunderlist.update_task(
    task_id=str(task['id']),
    task_revision=task['revision'],
    completed=True
  )


def process_trello_renamed_card(data):
  entities = data['action']['display']['entities']
  new_title = entities['card']['text']
  old_title = entities['name']['text']

  task = find_wunderlist_task(old_title)
  if not task: return
  wunderlist.update_task(
    task_id=str(task['id']),
    task_revision=task['revision'],
    title=new_title
  )


def process_trello_created_card(data):
  entities = data['action']['display']['entities']
  title = entities['card']['text']

  if find_wunderlist_task(title): return

  inbox_id = get_wunderlist_inbox_id()
  wunderlist.create_task(list_id=inbox_id, title=title)


def process_trello_archived_card(data):
  entities = data['action']['display']['entities']
  title = entities['card']['text']
  process_trello_completed_card(title)


def find_wunderlist_task(task_name):
  inbox_id = get_wunderlist_inbox_id()
  all_tasks = wunderlist.get_tasks(inbox_id)
  task = list(filter(lambda x: x['title'] == task_name, all_tasks))

  return task[0] if task else None


def process_wunderlist_hook(data):
  action = data['operation']
  task_data = data['data']
  subject = data.get('subject', {}).get('type')

  if not subject or subject != 'task': return

  if action == 'create':
    process_wunderlist_task_create_or_update(data, update=False)
  elif action == 'update':
    if 'completed' in task_data and task_data['completed']:
      process_wunderlist_completed_task(data)
    elif 'list_id' in task_data:
      process_wunderlist_completed_task(data)
    elif 'title' in task_data:
      process_wunderlist_renamed_task(data)
    elif 'starred' in task_data:
      process_wunderlist_prioritized_task(data, task_data['starred'])
    elif 'due_date' in task_data or 'remove' in task_data:
      process_wunderlist_task_create_or_update(data, update=True)


def process_wunderlist_task_create_or_update(data, update):
  task_data = data['data']
  title = data['after']['title']
  starred = task_data.get('starred')
  write = 'write' in title.lower()

  card = find_trello_card(title)
  if ((not update) and card) or (update and (not card)): return

  date_delta = get_wunderlist_task_due_date_delta(task_data)
  today, tomorrow = date_delta == 0, date_delta == 1

  lists = get_trello_list_ids()

  list_id = lists['Backlog']
  if write: list_id = lists['Write']
  elif today or starred: list_id = lists['Today']
  elif tomorrow: list_id = lists['Tomorrow']

  if update:
    trello.update_card(card_id=str(card['id']), list_id=list_id)
  else:
    trello.create_card(list_id=list_id, title=title)


def get_wunderlist_task_due_date_delta(task_data):
  due_date = task_data.get('due_date')
  if due_date:
    due_date = dateutil.parser.parse(due_date).date()
    return (due_date - datetime.datetime.now().date()).days
  return -1

def process_wunderlist_completed_task(data):
  task_data = data['before']
  title = task_data['title']

  card = find_trello_card(title)
  if not card: return

  done_list = get_trello_list_ids()['Done']

  trello.update_card(card_id=str(card['id']), list_id=done_list)


def process_wunderlist_prioritized_task(data, prioritized):
  task_data = data['before']
  title = task_data['title']

  card = find_trello_card(title)
  if not card: return

  lists = get_trello_list_ids()
  list = lists['Today'] if prioritized else lists['Backlog']

  trello.update_card(card_id=str(card['id']), list_id=list)


def process_wunderlist_renamed_task(data):
  before_title = data['before']['title']
  after_title = data['after']['title']

  card = find_trello_card(before_title)
  if not card: return

  trello.update_card(card_id=str(card['id']), title=after_title)


def find_trello_card(card_name):
  board_id = get_trello_today_board_id()
  all_cards = trello.get_cards(board_id)
  card = list(filter(lambda x: x['name'] == card_name, all_cards))

  return card[0] if card else None


@lru_cache()
def get_wunderlist_inbox_id():
  return wunderlist.get_lists()[0]['id']


@lru_cache()
def get_trello_today_board_id():
  return next(
    filter(lambda x: x['name'] == 'Today', trello.get_boards())
  )['id']


@lru_cache()
def get_trello_list_ids():
  names = ['Today', 'Tomorrow', 'Write', 'Backlog', 'Done']
  lists = trello.get_lists(get_trello_today_board_id())
  filtered = {
    list['name']: list['id']
    for list in lists if list['name'] in names
  }

  return filtered

if __name__ == '__main__':
  app.run(debug=True, port=9090)

