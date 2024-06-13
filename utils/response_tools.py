import utils.helpers as helpers

def handle_responses(msg, twitch_client, league_client) -> str:
    p_msg = msg.lower()

    if p_msg == "!time":
        return helpers.get_time()
    
    if p_msg == "!date":
        return helpers.get_date()
    
    if p_msg == "!test":
        return "what..."

    if p_msg.startswith("!get_userid"):
        user_string = p_msg.split(" ")[1].strip()
        userid = twitch_client.get_userid(user_string)
        return f"{user_string}'s userid is {userid}"
    
    if p_msg.startswith("!get_follower_count"):
        user_string = p_msg.split(" ")[1].strip()
        follower_count = twitch_client.get_follower_count(user_string)
        return f"{user_string}'s follower count is {follower_count}"
    
    if p_msg.startswith("!get_follower_count"):
        user_string = p_msg.split(" ")[1].strip()
        follower_count = twitch_client.get_follower_count(user_string)
        return f"{user_string}'s follower count is {follower_count}"
    
    if p_msg.startswith("!get_last_vod_timestamps"):
        user_string = p_msg.split(" ")[1].strip()
        vod_timestamps = twitch_client.get_last_vod_timestamps_string(user_string)
        return vod_timestamps
    
    if p_msg.startswith("!latestvod"):
        user_string = p_msg.split(" ")[1].strip()
        timestamps = twitch_client.get_last_vod_timestamps_string(user_string)
        vod_clips = twitch_client.get_latest_vod_clips(user_string)
        url = twitch_client.get_latest_streams('sleepy', 1)[0]['url']
        result = []
        result.append(timestamps)
        result.append(f"Vod link: {url}")
        result.append('Found timeline for the vod:')
        for i in vod_clips:
            stamped_url = url + f"?t={helpers.parse_twitch_timestamp(i['vod_offset'])}"
            result.append(f"**{i['view_count']} views** \n {i['duration']}s clip called: **{i['title']}** \n")
            result.append(f"starting at [{i['vod_offset']}]({stamped_url})\n")
            result.append(f"created by {i['creator_name']}:\n {i['url']}")
        return result
    
    if p_msg.startswith("!last_vod_opgg"):
        user_string = p_msg.split(" ")[1].strip()
        riot_id = p_msg.split(" ")[2].strip()
        region = p_msg.split(" ")[3].strip()
        puuid = league_client.getPUUIDByRiotID(riot_id, region)
        start_time, duration = twitch_client.get_last_vod_timestamps(user_string)
        end_time = helpers.parse_twitch_endtime(start_time, duration)
        startTime = helpers.parse_riot_epochtime(start_time)
        endTime = helpers.parse_riot_epochtime(end_time)
        print(startTime)
        print(endTime)
        matches = league_client.getMatchesByRiotID(riot_id, region, startTime=startTime, endTime=endTime)
        print(matches)
        url = twitch_client.get_latest_streams(user_string, 1)[0]['url']
        print(url)
        timestamp = ""
        result = []
        result.append(f"Found that {user_string} played {len(matches)} game(s) during that stream:")
        for match in matches:
            match_info, timestamp = league_client.getMatch(puuid=puuid, match_id=match, region=region)
            print(timestamp)
            processed_timestamp = int(timestamp) - int(startTime)
            stamped_url = url + f"?t={helpers.parse_twitch_timestamp(processed_timestamp)}"
            result.append((match_info, stamped_url))
        return result 
    else:
        return "unknown command, ignoring"