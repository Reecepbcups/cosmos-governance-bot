import requests, time

from ..utils.notifications import discord_notification

def get_max_archive_length(DISCORD_API, GUILD_ID, BOT_TOKEN_HEADERS_FOR_API, DISCORD_THREADS_AND_REACTIONS, THREAD_ARCHIVE_MINUTES, BOOSTED_DISCORD_THREAD_TIME_TIERS: dict) -> int:    
    if DISCORD_THREADS_AND_REACTIONS == False:
        return 0

    # Archive lengths are 1 or 24 hours for level 0 boosted servers, 3 days for level 1, and 7 days for level 2
    # Returns max time user
    v = requests.get(f"{DISCORD_API}/guilds/{GUILD_ID}", headers=BOT_TOKEN_HEADERS_FOR_API).json()    
    # print(v)
    
    if 'message' in v.keys() and v['message'] == '401: Unauthorized':
        print("Discord API Error: 401 Unauthorized. Please ensure you have the correct BOT_TOKEN set in secrets.json")
        exit()

    guildBoostLevel = int(v['premium_tier'])
    max_len = BOOSTED_DISCORD_THREAD_TIME_TIERS[guildBoostLevel]
    
    if THREAD_ARCHIVE_MINUTES not in [60, 1440, 4320, 10080]:
        THREAD_ARCHIVE_MINUTES = max_len
        print(f"\nInvalid thread archive length: {THREAD_ARCHIVE_MINUTES}")
        print(f"Using {max_len} minutes. Other options: [60, 1440, 4320, 10080]")
    elif THREAD_ARCHIVE_MINUTES > max_len:
        THREAD_ARCHIVE_MINUTES = max_len
        print(f"\nWARNING: THREAD_ARCHIVE_MINUTES is greater than the max archive length for this server. Setting to {max_len}")
        print(f"You need a higher boost level to use 4320 & 100080 sadly :(")

    return max_len

def get_last_msg_id(DISCORD_API, CHANNEL_ID, BOT_TOKEN_HEADERS_FOR_API):
    # gets last message from channel that the webhook just sent too. This way we can make thread from it without bot running all the time
    # https://discord.com/developers/docs/resources/channel#get-channel-messages
    res = requests.get(f"{DISCORD_API}/channels/{CHANNEL_ID}/messages?limit=1", headers=BOT_TOKEN_HEADERS_FOR_API).json()
    # print(res)
    return res[0]['id']

def discord_create_thread(message_id, thread_name, DO_ARCHIVE_THREADS: bool, THREAD_ARCHIVE_MINUTES: int, DISCORD_API, CHANNEL_ID, BOT_TOKEN_HEADERS_FOR_API):    
    data = { # https://discord.com/developers/docs/resources/channel#allowed-mentions-object-json-params-thread
        "name": thread_name,
        "archived": DO_ARCHIVE_THREADS,
        "auto_archive_duration": THREAD_ARCHIVE_MINUTES, # set via _SetMaxArchiveDurationLength on main() based on server boost level
        "locked": False,
        "invitable": False,
        "rate_limit_per_user": 5,
    }
    # print(data)
    # https://discord.com/developers/docs/topics/gateway#thread-create
    return requests.post(f"{DISCORD_API}/channels/{CHANNEL_ID}/messages/{message_id}/threads", json=data, headers=BOT_TOKEN_HEADERS_FOR_API).json()    


def discord_add_reacts(message_id, DISCORD_API, CHANNEL_ID, BOT_TOKEN_HEADERS_FOR_API, REACTION_RATE_LIMIT): # needs READ_MESSAGE_HISTORY & ADD_REACTIONS
    # https://discord.com/developers/docs/resources/channel#create-reaction
    # https://discord.com/developers/docs/resources/emoji    
    for emoji in ["✅", "❌", "⭕", "🚫"]:
        # print("PUT request for emoji: " + emoji) # DEBUGGING
        r = requests.put(f"{DISCORD_API}/channels/{CHANNEL_ID}/messages/{message_id}/reactions/{emoji}/@me", headers=BOT_TOKEN_HEADERS_FOR_API)
        if r.text != "":
            print(r.text)
        time.sleep(REACTION_RATE_LIMIT) # rate limit

def discord_post_to_channel(ticker, propID, title, description, voteLink, WEBHOOK_URL, HEX_COLOR, AVATAR_URL):
    # Auto replace description's <br> & \n ?
    if len(description) > 4096:
        description = description[:4090] + "..."

    discord_notification(
        url=WEBHOOK_URL,
        title=f"${str(ticker).upper()} #{propID} | {title}", 
        description=description,
        color=HEX_COLOR,
        values={"vote": [voteLink, False]},
        imageLink=AVATAR_URL,                      
    )