from random import choice
import requests
import json
from bs4 import BeautifulSoup

_user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
]


class ScrapperHelper(object):

    @staticmethod
    def random_agent(user_agents=None):
        if user_agents and isinstance(user_agents, list):
            return choice(user_agents)
        return choice(_user_agents)

    @staticmethod
    def get_response_from_url(url, proxy=None):
        try:
            response = requests.get(url, headers={'User-Agent': ScrapperHelper.random_agent()}, proxies={'http': proxy,
                                                                                                         'https': proxy})
            response.raise_for_status()
        except requests.HTTPError:
            raise requests.HTTPError('Received non 200 status code from Instagram')
        except requests.RequestException:
            raise requests.RequestException
        else:
            return response.text

    @staticmethod
    def extract_json_data_from_html(html):
        soup = BeautifulSoup(html, 'html.parser')
        body = soup.find('body')
        script_tag = body.find('script')
        raw_string = script_tag.text.strip().replace('window._sharedData =', '').replace(';', '')
        return json.loads(raw_string)
