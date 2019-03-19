import requests

class WunderApi(object):

  BASE_URL = 'https://a.wunderlist.com/api/v1'

  def __init__(self, access_token, client_id):
    self.headers = {
      'X-Access-Token' : access_token,
      'X-Client-ID' : client_id
    }


  def result(self, request):
    if request.status_code == 200: return request.json()
    else: return request.text


  def get_lists(self):
    url = '/'.join([self.BASE_URL, 'lists'])
    r = requests.get(url, headers=self.headers)
    return self.result(r)


  def get_tasks(self, list_id):
    url = '/'.join([self.BASE_URL, 'tasks']) + '?list_id=%d' % list_id
    r = requests.get(url, headers=self.headers)
    return self.result(r)

  def create_task(self, list_id, title):
    url = '/'.join([self.BASE_URL, 'tasks'])
    payload = {
      'list_id': list_id,
      'title': title,
      'pos': 'top'
    }
    r = requests.post(url, json=payload, headers=self.headers)
    return self.result(r)


  def update_task(self, task_id, task_revision, title=None, starred=None, completed=None):
    url = '/'.join([self.BASE_URL, 'tasks', task_id])

    payload = {}
    payload['revision'] = task_revision
    if title: payload['title'] = title
    if starred: payload['starred'] = starred
    if completed: payload['completed'] = completed

    r = requests.patch(url, json=payload, headers=self.headers)
    return self.result(r)
