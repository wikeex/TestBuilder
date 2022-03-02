import requests
from typing import Dict


class BaseClient:
    def __init__(self, endpoint: str):
        self.endpoint = endpoint
        self.session = requests.session()

    def get(self, path: str, **kwargs) -> Dict:
        return self.session.get(self.endpoint + path, **kwargs).json()

    def post(self, path: str, data=None, json=None, update_cookies=False, **kwargs) -> Dict:
        response = self.session.post(self.endpoint + path,  data=data, json=json, **kwargs)
        if update_cookies is True:
            self.session.cookies.update(response.cookies)
        return response.json()

