import discord, json, requests, time
from discord import Webhook, RequestsWebhookAdapter

DISCORD_API = "https://discord.com/api/v9"

with open('test-secrets.json', 'r') as f:
    secrets = json.load(f)

    discSecrets = secrets['DISCORD']
    WEBHOOK_URL = discSecrets['WEBHOOK_URL']
    USERNAME = discSecrets['USERNAME']
    AVATAR_URL = discSecrets['AVATAR_URL']
    HEX_COLOR = int(discSecrets['HEX_COLOR'], 16)

    discTreads = secrets['DISCORD_THREADS']
    CHANNEL_ID = int(discTreads['CHANNEL_ID'])
    GUILD_ID = int(discTreads['GUILD-SERVER_ID'])
    DO_ARCHIVE_THREADS = bool(discTreads['ARCHIVE_THREADS'])
    THREAD_ARCHIVE_MINUTES = int(discTreads['THREAD_ARCHIVE_MINUTES'])
    BOT_TOKEN = discTreads['BOT_TOKEN']                 
    BOT_TOKEN_HEADERS_FOR_API = {
        "Content-Type": "application/json",
        "authorization": "Bot " + BOT_TOKEN,    
    }


def discord_add_reacts(message_id): # needs READ_MESSAGE_HISTORY & ADD_REACTIONS
    # https://discord.com/developers/docs/resources/channel#create-reaction
    # https://discord.com/developers/docs/resources/emoji    
    for emoji in ["✅", "❌", "⭕", "🚫"]:
        print("PUT request for emoji: " + emoji)
        r = requests.put(f"{DISCORD_API}/channels/{CHANNEL_ID}/messages/{message_id}/reactions/{emoji}/@me", headers=BOT_TOKEN_HEADERS_FOR_API)
        if r.text != "":
            print(r.text)
        time.sleep(0.075) # rate limit

myMsg = "952769190140444724"
discord_add_reacts(myMsg)