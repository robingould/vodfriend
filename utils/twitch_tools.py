import os
import json
import utils.helpers as helpers
import requests
from dotenv import load_dotenv

load_dotenv()

TWITCH_API_KEY = os.getenv("TWITCH_API_KEY")
TWITCH_CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
TWITCH_ACCESS_TOKEN = os.getenv("TWITCH_ACCESS_TOKEN")
TWITCH_STATE = os.getenv("TWITCH_STATE")
REDIRECT_URI = os.getenv("REDIRECT_URI", "http://localhost")

class TwitchClient:
    """
    The Twitch API client class interacts with Twitch's API
    """
    def __init__(self):
        self.authorization_url = 'https://id.twitch.tv/'
        self.request_url = 'https://api.twitch.tv/helix/'

        self.access_token = TWITCH_ACCESS_TOKEN
        
        self.grant_type = 'client_credentials'
        self.headers = {
                        'Authorization': f'Bearer {self.access_token}'
                        }

        self.session = requests.Session()
        self.session.headers.update({'Authorization': f'Bearer {self.access_token}', 'Client-Id': TWITCH_CLIENT_ID})
        
    def update_headers(self):
        self.session.headers.update({'Authorization': f'Bearer {self.access_token}'})

    def get_token(self):
        """Handle grant flow for client credentialization 
        https://dev.twitch.tv/docs/authentication/getting-tokens-oauth/#client-credentials-grant-flow
        """
        url = f"{self.authorization_url}oauth2/token?client_id={TWITCH_CLIENT_ID}&client_secret={TWITCH_API_KEY}&grant_type={self.grant_type}"
        post_result = self.session.post(url)
        self.access_token = post_result.json()['access_token']
        self.update_headers()
        

    def get_userid(self, login: str) -> str:
        """Take in Twitch login name and return their userid
        """
        url = f"{self.request_url}users?login={login}"
        
        response = self.session.get(url)
        if response.status_code == 401:
            print("Token expired, retrying...")
            self.get_token()
            return self.get_userid(login)
                
        response.raise_for_status()
        
        data = response.json()['data']
            
        if len(data) == 0:
            Exception("Login doesn't exist!")
        return data[0]['id']
    
    # Analytics methods
    def get_follower_count(self, login:str) -> int:
        user_id = self.get_userid(login)
        url = f'{self.request_url}channels/followers?broadcaster_id={user_id}'
        response = self.session.get(url).json()
        count = response['total']
        return count
    
    def get_latest_streams(self, login: str, num_streams: int = 20) -> json:
        user_id = self.get_userid(login)
        url = f'{self.request_url}videos?user_id={user_id}&sort=time&type=archive&first={str(num_streams)}'
        latest_streams = self.session.get(url).json()
        return latest_streams['data']
    
    def get_latest_vod_views(self, login: str, num_streams: int = 20) -> list:
        latest_streams = self.get_latest_streams(login, num_streams)
        views = [(login, f'last {num_streams} view counts')]
        for vod in latest_streams:
            start_time = vod['created_at']
            view_count = vod['view_count']
            views.append((start_time, view_count))
        return views
    
    def get_latest_clips(self, login: str, num_clips: int = 20) -> json:
        user_id = self.get_userid(login)
        url = f'{self.request_url}clips?broadcaster_id={user_id}&sort=time&first={str(num_clips)}'
        latest_clips = self.session.get(url).json()
        return latest_clips

    def get_clips_between(self, login: str, started_at: str, ended_at: str) -> json:
        user_id = self.get_userid(login)
        url = f'{self.request_url}clips?broadcaster_id={user_id}&sort=time&started_at={started_at}&ended_at={ended_at}'
        clips = self.session.get(url).json()
        return clips['data']
    
    def get_latest_clip_views(self, login: str, num_clips: int = 20) -> list:
        latest_clips = self.get_latest_clips(login, num_clips)
        views = [(login, f'last {num_clips} view counts')]
        for clip in latest_clips:
            start_time = clip['created_at']
            view_count = clip['view_count']
            views.append((start_time, view_count))
        return views
    
    # Niche use cases
    def get_last_vod_timestamps(self, login: str):
        latest_vod = self.get_latest_streams(login, num_streams=1)
        start_time = latest_vod[0]['created_at']
        duration = latest_vod[0]['duration']
        response_string = f"{login} last started streaming at {start_time} and streamed for {duration}"
        print(response_string)
        return start_time, duration
    
    def get_last_vod_timestamps_string(self, login: str):
        latest_vod = self.get_latest_streams(login, num_streams=1)
        start_time = latest_vod[0]['created_at']
        duration = latest_vod[0]['duration']
        response_string = f"{login} last started streaming at {start_time} and streamed for {duration}"
        return response_string
    
    def get_latest_vod_clips(self, login: str):
        start_time, duration = self.get_last_vod_timestamps(login)
        end_time = helpers.parse_twitch_endtime(start_time, duration)
        data = self.get_clips_between(login, start_time, end_time)
        return data

if __name__ == "__main__":
    tc = TwitchClient()
    tc.get_token()
    print(tc.get_latest_streams('sleepy', 1)[0]['url'])
    #print(tc.get_latest_vod_clips("sleepy"))
    