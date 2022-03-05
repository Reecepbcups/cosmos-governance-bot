#!/usr/bin/python3

'''
Reece Williams (Reecepbcups | PBCUPS Validator)
February 9th, 2022
- Twitter bot to monitor and report on COSMOS governance proposals

apt install pip
pip install requests tweepy schedule

*Get REST lcd's in chain.json from https://github.com/cosmos/chain-registry

todo:
- Reduce files into 1, open file & load to dict, then check values.
- Dump from dict to hashmap on close / exit / cancel (like bash trap command)
'''

import tweepy
import requests
import os
import schedule
import time

IN_PRODUCTION = True

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
    "bitsong": [ 
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
    "gravity": [  
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
        'https://api.secretapi.io/cosmos/gov/v1beta1/proposals',
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


with open("secrets.prop", "r") as f:
    secrets = f.read().splitlines()
    APIKEY = secrets[0]
    APIKEYSECRET = secrets[1]
    ACCESS_TOKEN = secrets[2]
    ACCESS_TOKEN_SECRET = secrets[3]
    f.close()

# Authenticate to Twitter & Get API
auth = tweepy.OAuth1UserHandler(APIKEY, APIKEYSECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)


def tweet(ticker, propID, title, voteEndTime=""):
    message = f"${str(ticker).upper()} | Proposal #{propID} | VOTING_PERIOD | {title} | {chainAPIs[ticker][1]}/{propID}"
    
    twitterAt = chainAPIs[ticker][2] # @'s blockchains official twitter
    if len(twitterAt) > 1:
        twitterAt = f'@{twitterAt}' if not twitterAt.startswith('@') else twitterAt
        message += f" | {twitterAt}"

    print(message)

    if IN_PRODUCTION:
        try:
            tweet = api.update_status(message)
            print(f"Tweet sent for {tweet.id}: {message}")
            # api.update_status(in_reply_to_status_id=tweet.id, status=f"Voting Ends: {voteEndTime}")
        except:
            print("Tweet failed due to being duplicate")
        

def betterTimeFormat(ISO8061) -> str:
    # Improve in future to be Jan-01-2022
    return ISO8061.replace("T", " ").split(".")[0]

def getAllProposals(ticker) -> list:
    # Makes request to API & gets JSON reply in form of a list
    props = []
    
    try:
        link = chainAPIs[ticker][0]
        response = requests.get(link, headers={
            'accept': 'application/json', 
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}, 
            params={'proposal_status': '2'})
        # print(response.url)
        props = response.json()['proposals']
    except Exception as e:
        print(f"Issue with request to {ticker}: {e}")
    return props

def getLatestProposalIDChecked(ticker, fileName) -> int:
    # returns the last proposal ID we checked, or 0 if none tweeted yet
    lastPropID = 0

    # open text file (means we have already tweeted about this chain)
    if os.path.exists(fileName):
        with open(fileName, "r") as f:
            # update to last checked proposal ID
            lastPropID = int(f.read())
            f.close()
            
    print(f"{ticker} last voting prop id: {lastPropID}")

    return lastPropID

def checkIfNewestProposalIDIsGreaterThanLastTweet(ticker):
    fileName = f"{ticker}.txt"

    # get our last tweeted proposal ID (that was in voting period), found in file
    lastPropID = getLatestProposalIDChecked(ticker, fileName)

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

            # save newest prop ID to file so we don't double tweet it
            if IN_PRODUCTION:
                with open(fileName, "w") as f:
                    f.write(str(current_prop_id))
                    f.close()
            else:
                print("Not in production, not writing to file.")
                    
            # Tweet that bitch
            tweet(
                ticker=ticker,
                propID=current_prop_id, 
                title=prop['content']['title'], 
                # votePeriodEnd=betterTimeFormat(prop['voting_end_time'])
            )

def runChecks():
    for chain in chainAPIs.keys():
        try:
            checkIfNewestProposalIDIsGreaterThanLastTweet(chain)
        except Exception as e:
            print(f"{chain} checkProp failed: {e}")

    print(f"All chains checked {time.ctime()}, waiting") # pretty time output


SCHEDULE_SECONDS = 3
output = "Bot is in test mode..."

if IN_PRODUCTION:  
    SCHEDULE_SECONDS = 30*60 # every 30 mins
    output = "[!] BOT IS RUNNING IN PRODUCTION MODE!!!!!!!!!!!!!!!!!!"
    print(output)
    time.sleep(5) # Extra wait to ensure we want to run
    runChecks() # Runs 1st time to update, then does runnable


print(output)
schedule.every(SCHEDULE_SECONDS).seconds.do(runChecks)    
while True:
    schedule.run_pending()
    time.sleep(SCHEDULE_SECONDS)