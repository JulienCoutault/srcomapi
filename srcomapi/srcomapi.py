import requests
from http.client import responses
from os.path import dirname
from os import environ
import inspect

import srcomapi
import srcomapi.datatypes as datatypes
from .exceptions import APIRequestException, APINotProvidedException

with open(dirname(srcomapi.__file__) + "/.version") as f:
    __version__ = f.read().strip()
API_URL = "https://www.speedrun.com/api/v1/"
DEBUG = environ.get("DEBUG", None)

class SpeedrunCom(object):
    def __init__(self, api_key=None, user_agent="blha303:srcomapi/"+__version__):
        self._datatypes = {v.endpoint:v for k,v in inspect.getmembers(datatypes, inspect.isclass) if hasattr(v, "endpoint")}
        self.api_key = api_key
        self.user_agent = user_agent

    def get(self, endpoint, **kwargs):
        headers = {"User-Agent": self.user_agent}
        if self.api_key:
            headers["X-API-Key"] = self.api_key
        kwargs.update({"headers": headers})
        if DEBUG: print(API_URL + endpoint)
        response = requests.get(API_URL + endpoint, **kwargs)
        if response.status_code == 404:
            raise APIRequestException("{} {}".format(response.status_code, responses[response.status_code]), response)
        return response.json()["data"]

    def get_game(self, id, **kwargs):
        """Returns a srcomapi.datatypes.Game object"""
        response = self.get("games/{}".format(id), **kwargs)
        return datatypes.Game(self, data=response)

    def get_games(self, **kwargs):
        """Returns a generator that yields srcomapi.datatypes.Game objects"""
        response = self.get("games", **kwargs)
        for game_data in response:
            yield datatypes.Game(self, data=game_data)