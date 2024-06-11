import os
import discord
import utils.twitch_tools as twitch_tools
import utils.league_tools as league_tools
import utils.response_tools as response_tools
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

async def send_message(message, user_message, is_private, twitch_client, league_client):
    try:
        response = response_tools.handle_responses(user_message, twitch_client, league_client)
        #print(response)
        if isinstance(response, list):        
            for msg in response:
                await message.author.send(msg) if is_private else await message.channel.send(msg)
        else:
            await message.author.send(response) if is_private else await message.channel.send(response)
    
    except Exception as e:
        print(e)

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True


def run_bot():
    client = discord.Client(intents=intents)
    twitch_client = twitch_tools.TwitchClient()
    twitch_client.get_token()
    
    league_client = league_tools.LeagueClient()
    
    
    @client.event
    async def on_ready():
        print(f'{client.user} is READY ! !')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return 
        
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f"{username} said: '{user_message}' in ({channel})")

        if user_message[0] == '?':
            user_message = user_message[1:]
            await send_message(message, user_message, is_private=True, twitch_client=twitch_client, league_client=league_client)
        else:
            await send_message(message, user_message, is_private=False, twitch_client=twitch_client, league_client=league_client)

    client.run(TOKEN)
    