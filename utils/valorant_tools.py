import os
import requests
from dotenv import load_dotenv
from urllib.parse import urlencode

load_dotenv()

RIOT_SECRET = os.getenv("RIOT_SECRET")
RIOT_URL = os.getenv("RIOT_URL", f"https://americas.api.riotgames.com")
VALORANT_REGION = "NA"

class ValorantClient:
    def __init__(self):
        self.token = RIOT_SECRET
        
    def _query(self, input: list = []):
        params = {
            'api_key': RIOT_SECRET,
        }
        for i in input:
            params[i[0]] = i[1]
        
        return params
        
    def _sendRequest(self, url: str, params: dict = None) -> str | None:
        """
        Sends GET request to some url, with a dict of optional query parameters.
        """
        try:
            response = requests.get(url, params=urlencode(params))
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Issue getting match data from summoner: {e}")
            return None

    def getAccountByRiotID(self, riot_id: str, region: str) -> str | None:
        """
        riot_id is a string in the form: game_name#tag_line
        region is a string naming the region in the form "americas" or "europe", for the riot api url
        
        returns: a player's account in json form or None if it can't find an account. 
                Looks like {'puuid': {puuid}, 'gameName': {game_name}, 'tagLine': {tag_line}}
        """
        params = self._query()
        game_name, tag_line = riot_id.split("#")

        url = f"https://{region}.api.riotgames.com/valorant/v1/account/{game_name}/{tag_line}"
        
        return self._sendRequest(url=url, params=params)
        
    def getAccountByPUUID(self, puuid: str, region: str) -> str | None:
        """
        puuid the unique player id is a string that is 72 characters long
        region is a string naming the region in the form "americas" or "europe", for the riot api url
        
        returns: a player's account in json form or None if it can't find an account. 
                Looks like {'puuid': {puuid}, 'gameName': {game_name}, 'tagLine': {tag_line}}
        """
        params = self._query()
        url = f"https://{region}.api.riotgames.com/valorant/v1/by-puuid/account/{puuid}/"
        
        return self._sendRequest(url=url, params=params)

    "TODO: figure out kwargs for production grade api access for Match v1"
    def getMatchesByPUUID(self, puuid: str, region: str, **kwargs) -> list | None:
        """
        puuid the unique player id is a string that is 72 characters long
        region is a string naming the region in the form "americas" or "europe", for the riot api url
        **kwargs:
        
            
        returns: a list in the form ['RegionAbbrev_MatchID', ...]
                Example: for count = 5: ['NA1_5013210889', 'NA1_5013180841', 'NA1_5013154470', 'NA1_5012784554', 'NA1_5012776246']
        """
        filter = kwargs.get('filter', None)
        map = kwargs.get('map', None)
        size = kwargs.get('size', None)
        
        input = []
        if filter != None:
            input.append(('filter', filter))
            
        if map != None:
            input.append(('map', map))
        
        if size != None:
            input.append(('size', size))
        
        params = self._query(input)
        
        url = f"https://{region}.api.riotgames.com/valorant/v3/by-puuid/matches/{region}/{puuid}"
        
        return self._sendRequest(url=url, params=params)

    "TODO: figure out kwargs for production grade api access for Match v1"
    def getMatchesByRiotID(self, riot_id: str, region: str , **kwargs) -> list | None:
        """
        riot_id is a string in the form: game_name#tag_line
        region is a string naming the region in the form "americas" or "europe", for the riot api url
        puuid the unique player id is a string that is 72 characters long
        **kwargs:
        
            
        returns: a list in the form ['RegionAbbrev_MatchID', ...]
                Example: for count = 5: ['NA1_5013210889', 'NA1_5013180841', 'NA1_5013154470', 'NA1_5012784554', 'NA1_5012776246']
        """
        game_name, tag_line = riot_id.split("#")
        filter = kwargs.get('filter', None)
        map = kwargs.get('map', None)
        size = kwargs.get('size', None)
        input = []
        if filter != None:
            input.append(('filter', filter))
            
        if map != None:
            input.append(('map', map))
        
        if size != None:
            input.append(('size', size))
        
        params = self._query(input)
        
        url = f"https://{region}.api.riotgames.com/valorant/v3/matches/{region}/{game_name}/{tag_line}"
        
        return self._sendRequest(url=url, params=params)
        
    def getContent(self, locale: str = 'en-US', region: str = 'americas') -> str:
        """
        Takes in locale of the form 'en-US'
        region is a string naming the region in the form "americas" or "europe", for the riot api url
        
        returns: ContentDto, refer to https://developer.riotgames.com/apis#val-content-v1/GET_getContent
        """
        params = self._query(locale)
        
        url = f"https://{region}.api.riotgames.com/valorant/v1/content"
        
        return self._sendRequest(url=url, params=params)

    def getStatus(self, region: str) -> str:
        """
        region is a string naming the region in the form "americas" or "europe", for the riot api url

        returns: PlatformDataDto, refer to https://developer.riotgames.com/apis#val-status-v1/GET_getPlatformData
        """
        url = f"https://{region}.api.riotgames.com/valorant/v1/status/{region}"
        
        return self._sendRequest(url)