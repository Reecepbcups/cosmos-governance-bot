#!/usr/bin/python3

'''
Reece Williams (Reecepbcups | PBCUPS Validator)
February 9th, 2022
- Twitter bot to monitor and report on COSMOS governance proposals

apt install pip
pip install requests tweepy schedule
'''

import json
import tweepy
import requests
import os
import schedule
import time

IN_PRODUCTION = True

pingPubName = {
    # https://ping.pub/{VALUE}/gov/propID
    'dig': 'dig',
    'juno': 'juno',
    'huahua': 'chihuahua',
    'osmo': 'osmosis',
    'atom': 'cosmos',
    'akash': "akash-network",
    'star': 'stargaze',
    'kava': 'kava',
    'like': 'likecoin',
    'persistence': 'persistence',
}

chainAPIs = {
    "dig": 'https://api-1-dig.notional.ventures/cosmos/gov/v1beta1/proposals',
    'juno': 'https://lcd-juno.itastakers.com/cosmos/gov/v1beta1/proposals',
    'huahua': 'https://api.chihuahua.wtf/cosmos/gov/v1beta1/proposals',
    'osmo': 'https://osmo.api.ping.pub/cosmos/gov/v1beta1/proposals',
    'atom': 'https://cosmos.api.ping.pub/cosmos/gov/v1beta1/proposals',
    'akash': 'https://akash.api.ping.pub/cosmos/gov/v1beta1/proposals',
    'star': "https://rest.stargaze-apis.com/cosmos/gov/v1beta1/proposals",
    'kava': 'https://api.data.kava.io/cosmos/gov/v1beta1/proposals',
    'like': 'https://mainnet-node.like.co/cosmos/gov/v1beta1/proposals',
    'persistence': 'https://rest.core.persistence.one/cosmos/gov/v1beta1/proposals',
}


with open("secrets.prop", "r") as f:
    secrets = f.read().splitlines()
    APIKEY = secrets[0]
    APIKEYSECRET = secrets[1]
    ACCESS_TOKEN = secrets[2]
    ACCESS_TOKEN_SECRET = secrets[3]

# Authenticate to Twitter & Get API
auth = tweepy.OAuth1UserHandler(APIKEY, APIKEYSECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)


def tweet(chainSymbol, propID, title, voteEndTime=""):
    message = f"${str(chainSymbol).upper()} | Proposal #{propID} | VOTING_PERIOD | {title} | https://ping.pub/{pingPubName[chainSymbol]}/gov/{propID}"
    print(message)

    if IN_PRODUCTION:
        try:
            tweet = api.update_status(message)
            print(f"Tweet sent for {tweet.id}: {message}")
            # api.update_status(in_reply_to_status_id=tweet.id, status=f"Voting Ends: {voteEndTime}")
        except:
            print("Tweet failed due to being duplicate")
        

def betterTimeFormat(ISO8061):
    # Improve in future to be Jan-01-2022
    return ISO8061.replace("T", " ").split(".")[0]

def getAllProposals(chainSymbol):
    # Makes request to API & gets JSON reply, has to be a user-agent so nginx doesn't block connection
    
    link = chainAPIs[chainSymbol]
    p = {'proposal_status': '2'} # voting period

    # ping.pub API requires us to get directly
    # if chainSymbol in ['osmo', 'atom']:
    #     p =  # voting period

    try:
        response = requests.get(chainAPIs[chainSymbol], headers={
            'accept': 'application/json', 
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'}, 
            params=p)
        # print(response.url)
        props = response.json()['proposals']
    except Exception as e:
        print(f"Issue with request to {chainSymbol}: {e}")
        props = []
    return props

def getNewestProposalID(proposalsJSON) -> int:
    # Returns last proposal id int
    try:
        lastID = int(proposalsJSON[-1]['proposal_id'])
    except:
        lastID = -2
    return lastID

def getLatestProposalIDChecked(chainSymbol, fileName) -> int:
    # returns the last proposal ID we checked, or 0 if none tweeted yet
    lastPropID = 0

    # open text file (means we have already tweeted about this chain)
    if os.path.exists(fileName):
        with open(fileName, "r") as f:
            # update to last checked proposal ID
            lastPropID = int(f.read())
            
    print(f"{chainSymbol} last voting prop id: {lastPropID}")

    return lastPropID

def checkIfNewestProposalIDIsGreaterThanLastTweet(chainSymbol):
    fileName = f"{chainSymbol}.txt"

    # get our last tweeted proposal ID (that was in voting period)
    lastPropID = getLatestProposalIDChecked(chainSymbol, fileName)

    # gets JSON list of all proposals
    props = getAllProposals(chainSymbol)

    newestPropID = getNewestProposalID(props)

    if newestPropID == -1:
        # means there are no pending voting
        return

    # loop through out last stored voted prop ID & newest proposal ID
    for prop in props[lastPropID:newestPropID]:
        
        # only show gov proposals you can vote on
        if prop['status'] != "PROPOSAL_STATUS_VOTING_PERIOD":
            continue

        current_prop_id = int(prop['proposal_id'])

        # If this is a new proposal which is not the last one we tweeted for
        if current_prop_id > lastPropID:   

            print(f"Newest prop ID {current_prop_id} is greater than last prop ID {lastPropID}")

            # save newest prop ID to file so we don't double tweet it
            with open(fileName, "w") as f:
                f.write(str(current_prop_id))
                
            # Tweet that bitch
            tweet(
                chainSymbol=chainSymbol,
                propID=prop['proposal_id'], 
                title=prop['content']['title'], 
                # votePeriodEnd=betterTimeFormat(prop['voting_end_time'])
            )


def runChecks():
    for chain in chainAPIs.keys():
        # try:
        checkIfNewestProposalIDIsGreaterThanLastTweet(chain)
        # except Exception as e:
        #     print(f"{chain} checkProp failed: {e}")


SCHEDULE_SECONDS = 1 # 1 second for testing
output = "Bot is in test mode..."


if IN_PRODUCTION:  
    SCHEDULE_SECONDS = 10*60 # 5 minutes for prod.
    output = "[!] BOT IS RUNNING IN PRODUCTION MODE!!!!!!!!!!!!!!!!!!"
    print(output)
    time.sleep(5) # Extra wait to ensure we want to run
    runChecks() # Runs 1st time to update, then does runnable


print(output)
schedule.every(SCHEDULE_SECONDS).seconds.do(runChecks)    
while True:
    schedule.run_pending()
    time.sleep(SCHEDULE_SECONDS)