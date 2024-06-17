from chat_downloader import ChatDownloader

url = 'https://www.twitch.tv/videos/2171804738'
chat = ChatDownloader().get_chat(url)       # create a generator
with open('chat.txt', mode='w', newline='') as file:
    for message in chat:                        # iterate over messages
        file.write(chat.format(message) + '\n')  
    