import os
import requests
from dotenv import load_dotenv
from urllib.parse import urlencode

load_dotenv(override=True)

RIOT_SECRET = os.getenv("RIOT_SECRET")
RIOT_URL = os.getenv("RIOT_URL", f"https://americas.api.riotgames.com")

class LeagueClient:
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
        
    def getPUUIDByRiotID(self, riot_id: str, region: str) -> str:
        """
        riot_id is a string in the form: game_name#tag_line
        region is a string naming the region in the form "americas" or "europe", for the riot api url
             
        returns: puuid the unique player id is a string that is 72 characters long
        """
        params = self._query()
        game_name, tag_line = riot_id.split("#")
        url = f"https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
        return self._sendRequest(url=url, params=params)['puuid']
    
    def getAccountByRiotID(self, riot_id: str, region: str) -> str | None:
        """
        riot_id is a string in the form: game_name#tag_line
        region is a string naming the region in the form "americas" or "europe", for the riot api url
        
        returns: a player's account in json form or None if it can't find an account. 
                Looks like {'puuid': {puuid}, 'gameName': {game_name}, 'tagLine': {tag_line}}
        """
        params = self._query()
        game_name, tag_line = riot_id.split("#")

        url = f"https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
        
        return self._sendRequest(url=url, params=params)
        
    def getAccountByPUUID(self, puuid: str, region: str) -> str | None:
        """
        puuid the unique player id is a string that is 72 characters long
        region is a string naming the region in the form "americas" or "europe", for the riot api url
        
        returns: a player's account in json form or None if it can't find an account. 
                Looks like {'puuid': {puuid}, 'gameName': {game_name}, 'tagLine': {tag_line}}
        """
        params = self._query()
        url = f"https://{region}.api.riotgames.com/riot/account/v1/accounts/by-puuid/{puuid}/"
        
        return self._sendRequest(url=url, params=params)

    def getMatchesByPUUID(self, puuid: str, region: str, **kwargs) -> list:
        """
        puuid the unique player id is a string that is 72 characters long
        **kwargs:
            startTime:  long    Epoch timestamp in seconds. The matchlist started storing timestamps on June 16th, 2021. Any matches played before June 16th, 2021 won't be included in the results if the startTime filter is set.
            endTime:    long    Epoch timestamp in seconds.
            type:       string 	Filter the list of match ids by the type of match. This filter is mutually inclusive of the queue filter meaning any match ids returned must match both the queue and type filters.
            count:      int 	Defaults to 20. Valid values: 0 to 100. Number of match ids to return.
        
        returns: a list in the form ['RegionAbbrev_MatchID', ...]
                Example: for count = 5: ['NA1_5013210889', 'NA1_5013180841', 'NA1_5013154470', 'NA1_5012784554', 'NA1_5012776246']
        """
        startTime = kwargs.get('startTime', None)
        endTime = kwargs.get('endTime', None)
        type = kwargs.get('type', None)
        count = kwargs.get('count', None)
        input = []
        if startTime != None:
            input.append(('startTime', startTime))
            
        if endTime != None:
            input.append(('endTime', endTime))
        
        if type != None:
            input.append(('type', type))
        
        if count != None:
            input.append(('count', count))
        
        params = self._query(input)
        
        url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"
        
        return self._sendRequest(url=url, params=params)

    def getMatchesByRiotID(self, riot_id: str, region: str, **kwargs):
        """
        riot_id is a string in the form: game_name#tag_line
        region is a string naming the region in the form "americas" or "europe", for the riot api url
        **kwargs:
            startTime:  long    Epoch timestamp in seconds. The matchlist started storing timestamps on June 16th, 2021. Any matches played before June 16th, 2021 won't be included in the results if the startTime filter is set.
            endTime:    long    Epoch timestamp in seconds.
            type:       string 	Filter the list of match ids by the type of match. This filter is mutually inclusive of the queue filter meaning any match ids returned must match both the queue and type filters.
            count:      int 	Defaults to 20. Valid values: 0 to 100. Number of match ids to return.
        
        returns: a list of matchIds: string in the form ['matchId', ...]
                Example: for count = 5: ['NA1_5013210889', 'NA1_5013180841', 'NA1_5013154470', 'NA1_5012784554', 'NA1_5012776246']
        """
        puuid = self.getPUUIDByRiotID(riot_id, region)
        
        return self.getMatchesByPUUID(puuid, region, **kwargs)
        
    def getMatchTimeline(self, match_id: str, region: str) -> str | None:
        """
        matchIds:   string. Example: 'NA1_1234567890'
        
        returns: TimelineDto datatype as a string.
                refer to: https://developer.riotgames.com/apis#match-v5
        """
        params = self._query()
        url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/{match_id}/timeline"
        return self._sendRequest(url=url, params=params)
    
    def getMatch(self, puuid: str, match_id: str, region: str) -> str | None:
        params = self._query()
        url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/{match_id}"
        unprocessed_response = self._sendRequest(url=url, params=params)
        participants = unprocessed_response['info']['participants']
        result = ""
        for participant in participants:
            if participant['puuid'] == puuid:
                result = f"{participant['riotIdGameName']}#{participant['riotIdTagline']} played {participant['championName']}, reached level {participant['champLevel']} and placed {participant['placement']} and went {participant['kills']} kills {participant['deaths']} deaths {participant['assists']} assists"
        return result
