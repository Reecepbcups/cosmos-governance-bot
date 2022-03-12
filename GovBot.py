#!/usr/bin/python3

'''
Reece Williams (Reecepbcups | PBCUPS Validator) | February 9th, 2022
- Twitter bot to monitor and report on COSMOS governance proposals
- (Mar 8) Discord webhook to post proposals 
- (Mar 12) Discord Threads to allow for discussion of new proposals 

python3 -m pip install requests tweepy schedule discord

*Get REST lcd's in chain.json from https://github.com/cosmos/chain-registry
'''

import requests
import os
import schedule
import time
import json
import datetime

import discord
from discord import Webhook, RequestsWebhookAdapter

import tweepy

# When true, will actually tweet / discord post
IN_PRODUCTION = True
DISCORD = True
DISCORD_THREADS = True
TWITTER = False
# If false, it is up to you to schedule via crontab -e such as: */30 * * * * cd /root/twitterGovBot && python3 twitterGovernanceBot.py
USE_PYTHON_RUNNABLE = False
LOG_RUNS = False

# List of all APIS to check
chainAPIs = {
    "dig": [ 
        'https://api-1-dig.notional.ventures/cosmos/gov/v1beta1/proposals',
        'https://ping.pub/dig/gov',
        "@dig_chain"
        ],
    'juno': [
        'https://lcd-juno.itastakers.com/cosmos/gov/v1beta1/proposals',
        'https://ping.pub/juno/gov',
        ""
        ],
    'huahua': [
        'https://api.chihuahua.wtf/cosmos/gov/v1beta1/proposals',
        'https://ping.pub/chihuahua/gov',
        "@ChihuahuaChain"
        ],
    'osmo': [
        'https://lcd-osmosis.blockapsis.com/cosmos/gov/v1beta1/proposals',
        'https://ping.pub/osmosis/gov',
        '@osmosiszone'
        ],
    'atom': [
        'https://lcd-cosmoshub.blockapsis.com/cosmos/gov/v1beta1/proposals',
        'https://ping.pub/cosmos/gov',
        "@cosmos"
        ],
    'akt': [
        'https://akash.api.ping.pub/cosmos/gov/v1beta1/proposals',
        'https://ping.pub/akash-network/gov',
        '@akashnet_'
        ],
    'stars': [
        "https://rest.stargaze-apis.com/cosmos/gov/v1beta1/proposals",
        'https://ping.pub/stargaze/gov',
        '@StargazeZone'
        ],
    'kava': [
        'https://api.data.kava.io/cosmos/gov/v1beta1/proposals',
        'https://ping.pub/kava/gov',
        '@kava_platform'
        ],
    'like': [
        'https://mainnet-node.like.co/cosmos/gov/v1beta1/proposals',
        'https://ping.pub/likecoin/gov',
        '@likecoin'
        ],
    'xprt': [
        'https://rest.core.persistence.one/cosmos/gov/v1beta1/proposals',
        'https://ping.pub/persistence/gov',
        '@PersistenceOne'
        ],
    'cmdx': [
        'https://rest.comdex.one/cosmos/gov/v1beta1/proposals',
        'https://ping.pub/comdex/gov',
        '@ComdexOfficial'
        ],
    # New Adds:
    "bcna": [ 
        'https://lcd.bitcanna.io/cosmos/gov/v1beta1/proposals',
        'https://ping.pub/bitcanna/gov',
        '@BitCannaGlobal'
        ],
    "btsg": [ 
        'https://lcd-bitsong.itastakers.com/cosmos/gov/v1beta1/proposals',
        'https://ping.pub/bitsong/gov',
        '@BitSongOfficial'
        ],
    "band": [
        'https://laozi1.bandchain.org/api/cosmos/gov/v1beta1/proposals',
        'https://ping.pub/band-protocol/gov',
        '@BandProtocol'
        ],
    "boot": [ # Bostrom
        'https://lcd.bostrom.cybernode.ai/cosmos/gov/v1beta1/proposals',
        'https://ping.pub/bostrom/gov',
        ''
        ],
    "cheqd": [ 
        'https://api.cheqd.net/cosmos/gov/v1beta1/proposals',
        'https://ping.pub/cheqd/gov',
        '@cheqd_io'
        ],
    "cro": [  
        'https://mainnet.crypto.org:1317/cosmos/gov/v1beta1/proposals',
        'https://ping.pub/crypto-com-chain/gov',
        '@cryptocom'
        ],
    "evmos": [  
        'https://rest.bd.evmos.org:1317/cosmos/gov/v1beta1/proposals',
        'https://ping.pub/evmos/gov',
        '@EvmosOrg'
        ],
    "fetch": [
        'https://rest-fetchhub.fetch.ai/cosmos/gov/v1beta1/proposals',
        'https://www.mintscan.io/fetchai/proposals',
        '@Fetch_ai'
        ],
    "grav": [  
        'https://gravitychain.io:1317/cosmos/gov/v1beta1/proposals',
        'https://ping.pub/gravity-bridge/gov',
        '@gravity_bridge'
        ],
    "inj": [  
        'https://public.lcd.injective.network/cosmos/gov/v1beta1/proposals',
        'https://ping.pub/injective/gov',
        '@InjectiveLabs'
        ],
    "iris": [  
        'https://lcd-iris.keplr.app/cosmos/gov/v1beta1/proposals',
        'https://ping.pub/iris-network/gov',
        '@irisnetwork'
        ],
    'iov': [ #Starname
        "https://lcd-iov.keplr.app/cosmos/gov/v1beta1/proposals",
        'https://www.mintscan.io/starname/proposals',
        '@starname_me'
        ],
    "lum": [  
        'https://node0.mainnet.lum.network/rest/cosmos/gov/v1beta1/proposals',
        'https://ping.pub/LUM%20Network/gov',
        '@lum_network'
        ],
    "regen": [  
        'https://regen.stakesystems.io/cosmos/gov/v1beta1/proposals',
        'https://ping.pub/regen/gov',
        '@regen_network'
        ],
    "pb": [  
        'https://api.provenance.io/cosmos/gov/v1beta1/proposals',
        'https://ping.pub/provenance/gov',
        ''
        ],
    "secret": [  
        'https://api.scrt.network/cosmos/gov/v1beta1/proposals',
        'https://www.mintscan.io/secret/proposals',
        '@SecretNetwork'
        ],
    "sent": [  
        'https://lcd-sentinel.keplr.app/cosmos/gov/v1beta1/proposals',
        'https://ping.pub/sentinel/gov',
        '@Sentinel_co'
        ],
    "sif": [  
        'https://api.sifchain.finance:443/cosmos/gov/v1beta1/proposals',
        'https://ping.pub/sifchain/gov',
        "@sifchain"
        ],
    "terra": [  
        'https://blockdaemon-terra-lcd.api.bdnodes.net:1317/cosmos/gov/v1beta1/proposals',
        'https://ping.pub/terra-luna/gov',
        "@terra_money"
        ],
    "umee": [  
        'https://api.blue.main.network.umee.cc/cosmos/gov/v1beta1/proposals',
        'https://ping.pub/umee/gov',
        "@Umee_CrossChain"
        ],
}

# Don't touch below
proposals = {}
TICKERS_TO_ANNOUNCE = []
DISCORD_API = "https://discord.com/api/v9"
IS_FIRST_RUN = False
BOOSTED_DISCORD_THREAD_TIME_TIERS = {0: 1440,1: 4320,2: 10080,3: 10080}

with open('secrets.json', 'r') as f:
    secrets = json.load(f)

    TICKERS_TO_ANNOUNCE = secrets['TICKERS_TO_ANNOUNCE']
    filename = secrets['FILENAME']

    if TWITTER:
        twitSecrets = secrets['TWITTER']
        APIKEY = twitSecrets['APIKEY']
        APIKEYSECRET = twitSecrets['APIKEYSECRET']
        ACCESS_TOKEN = twitSecrets['ACCESS_TOKEN']
        ACCESS_TOKEN_SECRET = twitSecrets['ACCESS_TOKEN_SECRET']  
        # Authenticate to Twitter & Get API
        auth = tweepy.OAuth1UserHandler(APIKEY, APIKEYSECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth, wait_on_rate_limit=True)      

    if DISCORD:
        discSecrets = secrets['DISCORD']
        WEBHOOK_URL = discSecrets['WEBHOOK_URL']
        USERNAME = discSecrets['USERNAME']
        AVATAR_URL = discSecrets['AVATAR_URL']
        HEX_COLOR = int(discSecrets['HEX_COLOR'], 16)

        if DISCORD_THREADS:
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

def load_proposals_from_file() -> dict:
    global proposals
    with open(filename, 'r') as f:
        proposals = json.load(f)        
    return proposals

def save_proposals() -> None:
    if len(proposals) > 0:
        with open(filename, 'w') as f:
            json.dump(proposals, f)

def update_proposal_value(ticker, newPropNumber):
    global proposals
    proposals[ticker] = newPropNumber
    save_proposals()

def _SetMaxArchiveDurationLength() -> int:
    global THREAD_ARCHIVE_MINUTES
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

def discord_create_thread(message_id, thread_name):
    global DO_ARCHIVE_THREADS
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

def _getLastMessageID():
    # gets last message from channel that the webhook just sent too. This way we can make thread from it without bot running all the time
    # https://discord.com/developers/docs/resources/channel#get-channel-messages
    res = requests.get(f"{DISCORD_API}/channels/{CHANNEL_ID}/messages?limit=1", headers=BOT_TOKEN_HEADERS_FOR_API).json()
    # print(res)
    return res[0]['id']

def discord_post_to_channel(ticker, propID, title, description, chainExploreLink):
    embed = discord.Embed(title=f"${str(ticker).upper()} #{propID} | {title}", description=description, timestamp=datetime.datetime.utcnow(), color=HEX_COLOR) #color=discord.Color.dark_gold()
    embed.add_field(name="Link", value=f"{chainExploreLink}")
    embed.set_thumbnail(url=AVATAR_URL)
    webhook = Webhook.from_url(WEBHOOK_URL, adapter=RequestsWebhookAdapter()) # Initializing webhook
    webhook.send(username=USERNAME,embed=embed) # Executing webhook

def post_update(ticker, propID, title, description=""):
    chainExploreLink = f"{chainAPIs[ticker][1]}/{propID}"
    message = f"${str(ticker).upper()} | Proposal #{propID} | VOTING_PERIOD | {title} | {chainExploreLink}"
    
    twitterAt = chainAPIs[ticker][2] # @'s blockchains official twitter
    if len(twitterAt) > 1:
        twitterAt = f'@{twitterAt}' if not twitterAt.startswith('@') else twitterAt
        message += f" | {twitterAt}"
    print(message)

    if IN_PRODUCTION:
        try:
            if TWITTER:
                tweet = api.update_status(message)
                print(f"Tweet sent for {tweet.id}: {message}")
            if DISCORD:
                discord_post_to_channel(ticker, propID, title, description, chainExploreLink)
                if DISCORD_THREADS:
                    discord_create_thread(_getLastMessageID(), f"{ticker}-{propID}") 
                    pass
        except Exception as err:
            print("Tweet failed due to being duplicate OR " + str(err)) 
    
    
def getAllProposals(ticker) -> list:
    # Makes request to API & gets JSON reply in form of a list
    props = []
    
    try:
        link = chainAPIs[ticker][0]
        response = requests.get(link, headers={
            'accept': 'application/json', 
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}, 
            params={'proposal_status': '2'}) # 2 = voting period
        # print(response.url)
        props = response.json()['proposals']
    except Exception as e:
        print(f"Issue with request to {ticker}: {e}")
    return props

def checkIfNewestProposalIDIsGreaterThanLastTweet(ticker):
    # get our last tweeted proposal ID (that was in voting period), if it exists
    # if not, 0 is the value so we search through all proposals
    lastPropID = 0
    if ticker in proposals:
        lastPropID = int(proposals[ticker])

    # gets JSON list of all proposals
    props = getAllProposals(ticker)
    if len(props) == 0:
        return

    # loop through out last stored voted prop ID & newest proposal ID
    for prop in props:
        current_prop_id = int(prop['proposal_id'])

        # If this is a new proposal which is not the last one we tweeted for
        if current_prop_id > lastPropID:   
            print(f"Newest prop ID {current_prop_id} is greater than last prop ID {lastPropID}")
            
            if IS_FIRST_RUN or IN_PRODUCTION:      
                # save to proposals dict & to file (so we don't post again), unless its the first run                                 
                update_proposal_value(ticker, current_prop_id)
            else:
                print("Not in production, not writing to file.")

            post_update(
                ticker=ticker,
                propID=current_prop_id, 
                title=prop['content']['title'], 
                description=prop['content']['description'], # for discord embeds
            )

def logRun():
    if LOG_RUNS:
        with open("logs.txt", 'a') as flog:
            flog.write(str(time.ctime() + "\n"))

def runChecks():   
    print("Running checks...") 
    for chain in chainAPIs.keys():
        try:
            if chain not in TICKERS_TO_ANNOUNCE and TICKERS_TO_ANNOUNCE != []:
                continue

            checkIfNewestProposalIDIsGreaterThanLastTweet(chain)
        except Exception as e:
            print(f"{chain} checkProp failed: {e}")
    logRun()
    print(f"All chains checked {time.ctime()}, waiting")


def updateChainsToNewestProposalsIfThisIsTheFirstTimeRunning():
    global IN_PRODUCTION, IS_FIRST_RUN
    '''
    Updates JSON file to the newest proposals provided this is the first time running
    '''
    if os.path.exists(filename):
        print(f"{filename} exists, not updating")
        return

    IS_FIRST_RUN = True
    if IN_PRODUCTION:
        IN_PRODUCTION = False
        
    print("Updating chains to newest values since you have not run this before, these will not be posted")
    runChecks()
    save_proposals()
    print("Run this again now, chains have been populated")
    exit(0)

if __name__ == "__main__":        
    updateChainsToNewestProposalsIfThisIsTheFirstTimeRunning()

    load_proposals_from_file()    
    _SetMaxArchiveDurationLength()

    # informs user & setups of legnth of time between runs
    if IN_PRODUCTION:
        SCHEDULE_SECONDS = 30*60
        print("[!] BOT IS RUNNING IN PRODUCTION MODE!!!!!!!!!!!!!!!!!!")
        time.sleep(5)
        print(f"[!] Running {TICKERS_TO_ANNOUNCE} in 2 seconds")
        time.sleep(2)
    else:
        SCHEDULE_SECONDS = 3
        print("Bot is in test mode...")

    if DISCORD:
        print("DISCORD module enabled")
    if TWITTER:
        print("TWITTER module enabled")

    runChecks()

    # If user does not use a crontab, this can be run in a screen/daemon session
    if USE_PYTHON_RUNNABLE:      
        schedule.every(SCHEDULE_SECONDS).seconds.do(runChecks)  
        while True:
            print("Running runnable then waiting...")
            schedule.run_pending()
            time.sleep(SCHEDULE_SECONDS)
            

    
