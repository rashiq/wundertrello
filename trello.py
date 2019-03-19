import requests

class TrelloApi(object):

  BASE_URL = 'https://api.trello.com/1'

  def __init__(self, access_token, client_id):
    self.query_params = {
      'key' : access_token,
      'token' : client_id
    }

  def result(self, request):
    if request.status_code == 200: return request.json()
    else: return request.text


  def get_boards(self):
    url = '/'.join([self.BASE_URL, 'members', 'me', 'boards', 'all'])
    r = requests.get(url, params=self.query_params)
    return self.result(r)


  def get_lists(self, board_id):
    url = '/'.join([self.BASE_URL, 'boards', str(board_id), 'lists'])
    r = requests.get(url, params=self.query_params)
    return self.result(r)


  def get_cards(self, board_id):
    url = '/'.join([self.BASE_URL, 'boards', str(board_id), 'cards'])
    r = requests.get(url, params=self.query_params)
    return self.result(r)


  def create_card(self, list_id, title):
    url = '/'.join([self.BASE_URL, 'cards'])
    payload = self.query_params.copy()
    payload.update({
      'idList': list_id,
      'name': title,
      'pos': 'top'
    })
    r = requests.post(url, params=payload)
    return self.result(r)

  def update_card(self, card_id, title=None, list_id=None):
    url = '/'.join([self.BASE_URL, 'cards', str(card_id)])
    payload = self.query_params.copy()
    if title: payload['name'] = title
    if list_id: payload['idList'] = list_id

    r = requests.put(url, params=payload)
    return self.result(r)
