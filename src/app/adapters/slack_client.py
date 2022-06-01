import os
import requests
import json

USERS_TOKEN = { # What if users have same name? 아마 회사차원에서도 정현정1, 정현정2로 하지 않을까? 원티드 스페이스에서도 구분이 필요하니까. 
    "정현정": os.environ.get('JHJ_TOKEN'), # starts with 'xoxp-'
    "최경영": os.environ.get('CGY_TOKEN'),
}

class SlackClient:
  def __init__(self):
    self.users_token = USERS_TOKEN

  def _get_user_token(self, user_name):
    print("token", self.users_token[user_name])
    return self.users_token[user_name]


  def update_status(self, user_name, status):
    token = self._get_user_token(user_name)
    headers = {
        "Authorization": "Bearer " + token
    }
    url = "https://slack.com/api/users.profile.set" # https://api.slack.com/methods/users.profile.set
    data_str = json.dumps(status)
    params = {
        'profile': data_str
    }
    resp = requests.put(url, headers=headers, params=params)

    return resp.json()
