import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

class API(object):
    def __init__(self,url,jwt_token):
        self.url = url
        self.jwt_token = jwt_token

    def call(self):
        session = requests.Session()
        retries = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
        session.mount('https://', HTTPAdapter(max_retries=retries))

        # headers = {'Authorization': f'Bearer {jwt_token}'}
        # response = session.get(url, headers=headers)
        response = session.get(self.url)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

