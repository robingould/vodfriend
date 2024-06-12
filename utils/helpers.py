from datetime import datetime
from time import strftime, gmtime
import imgkit

def get_time():
    current_time = datetime.now()
    format = '%I:%M %p'   
    time_now = current_time.strftime(format)
    return time_now

def get_date():
    current_time = datetime.now()
    format = '%m/%d/%Y' 
    todays_date = current_time.strftime(format)
    return todays_date

import re
from datetime import datetime, timedelta

# State string helps prevent CSRF attacks. 
# If the state string returned by the server doesn't match, ignore the response
def check_url_state_for_CSRF(request_result, state):
    new_state = request_result.json()['state']

    if not new_state == state:
        raise Exception("Potential CRSF attack, new state sent by server didn't match sent state in auth request! https://owasp.org/www-community/attacks/csrf")

# Function to parse the timedelta string
def parse_timedelta(timedelta_str):
    pattern = re.compile(r'(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?')
    match = pattern.match(timedelta_str)
    
    if not match:
        raise ValueError("Invalid timedelta format")

    hours = int(match.group(1)) if match.group(1) else 0
    minutes = int(match.group(2)) if match.group(2) else 0
    seconds = int(match.group(3)) if match.group(3) else 0

    return timedelta(hours=hours, minutes=minutes, seconds=seconds)

def parse_twitch_endtime(start_time, duration):
    dt = datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%SZ")
    time_delta = parse_timedelta(duration)
    end_time_preprocessed = dt + time_delta
    end_time = end_time_preprocessed.strftime("%Y-%m-%dT%H:%M:%SZ")
    return end_time

def parse_twitch_timestamp(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours:02d}h{minutes:02d}m{seconds:02d}s"

def parse_riot_epochtime(timestamp):
    dt = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")

    # Convert to Unix epoch time
    epoch = int(dt.timestamp())
    
    return epoch

def parse_epochtime(timestamp):
    dtime = strftime('%Y-%m-%d %H:%M:%S', gmtime(timestamp))
    return dtime

def construct_match(puuid, unprocessed_response):
    participants = unprocessed_response['info']['participants']
    result = []
    timing = parse_epochtime(unprocessed_response['info']['gameEndTimestamp'])
    duration = parse_twitch_timestamp(unprocessed_response['info']['gameDuration'])
    found = 0
    for participant in participants:
        if puuid == participant['puuid']:
            print(puuid)
            found = 1
            tagline = f"{participant['riotIdGameName']}#{participant['riotIdTagline']}"
            champion_name = participant['championName']
            level = participant['champLevel']
            placement = participant['placement']
            
            if participant['win'] == True:
                win = 'Victory'
            else:
                win = "Defeat"
            kills = participant['kills'] 
            deaths = participant['deaths'] 
            assists = participant['assists']
            kda = participant['challenges']['kda']
            killParticipation = participant['challenges']['killParticipation']
            #summoner1Id = participant['summoner1Id']
            #summoner2Id = participant['summoner2Id']
            champion_image = f"https://ddragon.leagueoflegends.com/cdn/14.11.1/img/champion/{champion_name}.png"
            body = f"<div><img src={champion_image}> <div>{kills} / {deaths} / {assists} </div></div>"
            imgkit.from_string(body, 'out.jpg')
            return 'out.jpg'
            
            
    if found == 0:
        return "Error, couldn't find player"
    
            
    
    
    