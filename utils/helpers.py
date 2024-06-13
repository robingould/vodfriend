import re
import requests
from datetime import datetime, timedelta
from time import strftime, gmtime
import imgkit

version = '14.12.1'

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
    epoch = datetime(1970, 1, 1)
    epoch_time = int((dt - epoch).total_seconds())
    return epoch_time

def parse_epochtime(timestamp):
    dtime = strftime('%Y-%m-%d %H:%M:%S', gmtime(timestamp))
    return dtime

def ddragon_get_runes_dict(version):
    url = f"http://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/runesReforged.json"
    html = requests.get(url).json()
    #perk_dict = {item["id"]: item["key"] for item in html} #Domination (8100), Inspiration (8300), Precision (8000), Resolve (8400), Sorcery (8200)
    #rune_dict = {rune["id"]: rune["key"] for item in html for slot in item["slots"] for rune in slot["runes"]}
    big_dict = {item["id"]: item["icon"] for item in html}
    image_dict = {rune["id"]: rune["icon"] for item in html for slot in item["slots"] for rune in slot["runes"]}

    return big_dict | image_dict

def ddragon_get_summs_dict(version):
    url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/summoner.json"
    html = requests.get(url).json()['data']
    spell_dict = {html[spell]['key']: html[spell]['image']['full'] for spell in html}
    return spell_dict

def communitydragon_get_augments(version):
    url = f"https://raw.communitydragon.org/14.12/cdragon/arena/en_us.json"
    html = requests.get(url).json()['augments']
    augment_dict = {html[augment]['id']: html[augment]['iconLarge'] for augment, _ in enumerate(html)}
    return augment_dict
   
def construct_match(puuid, unprocessed_response, matchid):
    participants = unprocessed_response['info']['participants']
    timestamp = int(unprocessed_response['info']['gameStartTimestamp']/1000)
    result = []
    timing = parse_epochtime(unprocessed_response['info']['gameEndTimestamp']/1000)
    duration = parse_twitch_timestamp(unprocessed_response['info']['gameDuration'])
    game_type = unprocessed_response['info']['gameMode']
    found = 0
    for participant in participants:
        if puuid == participant['puuid']:
            found = 1
            tagline = f"{participant['riotIdGameName']}#{participant['riotIdTagline']}"
            champion_name = participant['championName']
            level = participant['champLevel']
            win = participant['win']
            kills = participant['kills'] 
            deaths = participant['deaths'] 
            assists = participant['assists']
            kda = round(participant['challenges']['kda'], 2)
            killParticipation = int(round(participant['challenges']['killParticipation'], 2)*100)
            game_color = 'red' if win == False else 'blue'
            result = 'Defeat' if win == False else 'Victory'
            background_color = ' pink' if win == False else 'lightblue'
            control_wards = ''
            placement = ''
            creep_score = ''
            cs_per_min = ''
            cs_div = ''
            kp = ''
            link1 = ''
            link2 = ''
            link3 = ''
            link4 = ''

            if 'CLASSIC' in game_type:
                game_type = "Ranked Solo/Duo"
                spells = ddragon_get_summs_dict(version)
                runes = ddragon_get_runes_dict(version)
                selection1 = participant['perks']['styles'][0]['selections'][0]['perk']
                selection2 = participant['perks']['styles'][1]['style']
                summoner1Id = str(participant['summoner1Id'])
                summoner2Id = str(participant['summoner2Id'])
                spell1 = spells[summoner1Id]
                spell2 = spells[summoner2Id]
                rune1 = runes[selection1]
                rune2 = runes[selection2]
                controlWardsPlaced = participant['challenges']['controlWardsPlaced']
                control_wards = f"<div class='ward'>Control Ward {controlWardsPlaced}</div>"
                creep_score = int(participant['totalMinionsKilled']) + int(participant['neutralMinionsKilled'])
                cs_per_min = round(creep_score / (participant['timePlayed']/60), 1)
                cs_div = f"<div style='position: relative;'>CS {creep_score} ({cs_per_min})</div>"
                link1 = f"https://ddragon.leagueoflegends.com/cdn/{version}/img/spell/{spell1}"
                link2 = f"https://ddragon.leagueoflegends.com/cdn/{version}/img/spell/{spell2}"
                link3 = f"https://ddragon.leagueoflegends.com/cdn/img/{rune1}"
                link4 = f"https://ddragon.leagueoflegends.com/cdn/img/{rune2}"
                kp = f""" <div class='p-kill' style='color: {game_color}'>
                                            <div style='position: relative;'>P/Kill {killParticipation}%</div>
                                        </div>
                                        """
            elif 'CHERRY' in game_type:
                game_type = "Arena"
                augments = communitydragon_get_augments(version)
                place = participant['placement']
                th_or_nd = 'nd' if place <= 2 else 'th'
                placement = f"<div style='position: relative;'>{place}{th_or_nd}</div>"
                playerAugment1_id = participant['playerAugment1'] if participant['playerAugment1'] != 0 else 93
                playerAugment2_id = participant['playerAugment2'] if participant['playerAugment2'] != 0 else 93
                playerAugment3_id = participant['playerAugment3'] if participant['playerAugment3'] != 0 else 93
                playerAugment4_id = participant['playerAugment4'] if participant['playerAugment4'] != 0 else 93
                playerAugment1 = augments[playerAugment1_id] 
                playerAugment2 = augments[playerAugment2_id]
                playerAugment3 = augments[playerAugment3_id]
                playerAugment4 = augments[playerAugment4_id]
                
                link1 = f"https://raw.communitydragon.org/latest/game/{playerAugment1}" 
                link2 = f"https://raw.communitydragon.org/latest/game/{playerAugment2}" 
                link3 = f"https://raw.communitydragon.org/latest/game/{playerAugment3}"
                link4 = f"https://raw.communitydragon.org/latest/game/{playerAugment4}"
            else:
                pass
            champion_image = f"https://ddragon.leagueoflegends.com/cdn/{version}/img/champion/{champion_name}.png"
            body = f"""
<!DOCTYPE html>
    <html>
    <head>
        <meta content="jpg"/>
        <meta  content="Landscape"/>
    </head>
    <body>
        <div class='container' style='display: flex; height: 100%; flex-direction: column; width: 100%; background-color: {background_color}; border-radius: 1px; overlow: hidden;'>
            <div class='deco' style='position: absolute; display: block; height: 84%; width: 6px; min-width: 6px; border-radius: 1px; background-color: {game_color};'></div> 
            <div class='inner' style='display: flex; flex-direction: column; min-width: 100%; width: 100%; gap: 8px; padding: 0px 12px; unicode-bidi: isolate'>
                <div class='left-section' style='margin-top: 3px; float: left; width: 108px; display: flex; flex-direction: column; gap: 8px; font-size: 12px; font-weight: 400; line-height: 16px; color: gray;'>
                        <div class='head-group' style='display: flex; flex-direction: column; white-space: nowrap; font-size: 12px; font-weight: 400; line-height: 16px; color: gray'>
                            <div class='game-type' style='font-weight: 700; display: block; white-space: nowrap; font-size: 12px; line-height: 16px; color: {game_color}'>{game_type}</div>
                            <div class='timestamp' style='display: block;font-size: 12px; font-weight: 400; line-height: 16px; color: gray; white-space: nowrap'>
                                <div style='position: relative;'>{timing}</div>
                            </div>
                        </div>
                        <div class='divider' style='margin-top: 5px; margin-bottom: 5px; width: 48px; height: 1px; background-color: {game_color}; opacity: 0.2; font-size: 12px; font-weight: 400; line-height: 16px; color: gray'></div>
                        <div class='head-group' style='display: flex; flex-direction: column; white-space: nowrap; font-size: 12px; font-weight: 400; line-height: 16px; color: gray'>
                            <div class='result' style='font-weight: 700; display: block; white-space: nowrap; line-height: 16px; color: {game_color}'>{result}</div>
                            <div class='length' style='display: block; white-space: nowrap; font-size: 12px; font-weight: 400; line-height: 16px; color: gray;'>{duration}</div>
                        </div>
                    </div> 
                </div>   
                <div class='middle-section' style='margin-top: 5px; margin-left: -20px; display: flex; flex-direction: column; float: left; -webkit-box-pack: start; justify-content: flex-start; height: 87%; gap: 2px; flex: 1 1 0%; font-size: 12px; max-height: 100%'>
                    <div class='main' style='display: flex; align-items: center; gap: 12px; display: flex; -webkit-box-align: center; align-items: center; gap: 4px; height: 58px; font-size: 12px;'>
                       <div class='info' style='display: flex; float: left; -webkit-box-align: center; align-items: center; gap: 4px; height: 58px; font-size: 12px; max-height:100px'>
                                        <div class='champion' style='position: relative; display: flex; -webkit-box-pack: center; justify-content: right; -webkit-box-align: center; align-items: right; min-width: 48px; '>
                                            <img src={champion_image} width='48' height='48' style='border-radius: 50%; border: 0; vertical-align: middle; max-width: 100%; width: 48px; aspect-ratio: auto 48 / 48; height: 48px; '>
                                            <span class='champion-level' style='position: absolute; left: 30px; bottom: 0px; display: inline-block; width: 20px; height: 20px; font-size: 11px; font-weight: 400; line-height: 14px; color: rgb(255, 255, 255); background: rgb(32, 45, 55); border-radius: 50%; text-align: center; line-height:18px'>{level}</span>
                                        </div>
                                        <div class='GameLoadout' style='position: absolute; left: 170px; bottom: 40px; display: flex; gap: 2px; font-size: 12px;'>
                                            <div class='loadout-group' style='display: flex; float:left; flex-direction: column; gap: 2px; font-size: 12px;'>
                                                <div class='spell' style='position: relative; display: flex; overflow: hidden; border-radius: 4px;'>
                                                    <img src='{link1}' width='22' height='22' style='background: rgb(0, 0, 0); border-radius: 4px;'>
                                                </div>
                                                <div class='spell' style='position: relative; display: flex; overflow: hidden; border-radius: 4px;'>
                                                    <img src='{link2}' width='22' height='22' style='background: rgb(0, 0, 0); border-radius: 4px;'>
                                                </div>
                                            </div>
                                            <div class='loadout-group' style='display: flex; float:right; flex-direction: column; gap: 2px; font-size: 12px;'>
                                                <div class='rune rune-primary' style='position: relative; display: flex; overflow: hidden; border-radius: 50%; font-size: 12px;'>
                                                    <img src='{link3}' width='22' height='22' style='background: rgb(0, 0, 0); aspect-ratio: 1 / 1; min-width: 22px; border: 0; vertical-align: middle; max-width: 100%;width: 22px; height: 22px; overflow-clip-margin: content-box; overflow: clip; border-radius: 50%;'>
                                                </div>
                                                <div class='rune rune-secondary' style='position: relative; display: flex; overflow: hidden; border-radius: 50%; font-size: 12px;'>
                                                    <img src='{link4}' width='22' height='22' style='background: rgb(0, 0, 0); aspect-ratio: 1 / 1; min-width: 22px; border: 0; vertical-align: middle; max-width: 100%;width: 22px; height: 22px; overflow-clip-margin: content-box; overflow: clip; border-radius: 50%;'>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                    <div class='kda-stats' style='width: 108px; position: absolute; margin-top: 5px; margin-left: 120px; display: flex; flex-direction: column; align-items: flex-start; gap: 2px; font-size: 12px;'>
                                        <div class='kda' style='color: gray; font-size: 15px; font-weight: 700; line-height: 22px; display: block;'>
                                            <span style='color: black; font-size: 15px; font-weight: 700; line-height: 22px;'>{kills}</span> / <span class='d' style='color: red; font-size: 15px; font-weight: 700; line-height: 22px;'>{deaths}</span> / <span style='color: black; font-size: 15px; font-weight: 700; line-height: 22px;'>{assists}</span>
                                        </div>
                                            <div class='kda-ratio' style='color: gray; font-size: 12px; font-weight: 400; line-height: 16px; display: block;'>{kda}:1 KDA</div>
                                        </div>
                                    
                    <div class='game-stats' style='position: absolute; margin-top: 5px; margin-left: 200px; display: flex; flex-direction: column; height: 58px; flex: 1 1 0%; padding-left: 8px; border-left-width: 1px; border-left-style: solid; border-color: {game_color}; color: gray; font-size: 11px; font-weight: 400; line-height: 14px;'>
                                        {kp}
                                        {placement}
                                        {control_wards}
                                        <div class='cs'>
                                            {cs_div}
                                        </div>
                                        <div class='avg-tier'>
                                            <div style='position: relative;'>low masta</div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            </div>

    </body>
    </html>"""
            options = {'height': 100, 'width': 540, 'disable-smart-width': ''}
            out = f'images/{matchid}.jpg'
            imgkit.from_string(body, out, options=options)
            return out, timestamp
            
    if found == 0:
        return "Error, couldn't find player"
