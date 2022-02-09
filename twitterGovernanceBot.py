#!/usr/bin/python3

'''
Reece Williams (Reecepbcups | PBCUPS Validator)
February 9th, 2022
- Twitter bot to monitor and report on COSMOS governance proposals

apt install pip
pip install request tweepy schedule
'''

import tweepy
import requests
import os
import schedule
import time


IN_PRODUCTION = False

pingPubName = {
    'dig': 'dig',
    'juno': 'juno',
    'huahua': 'chihuahua',
    'osmo': 'osmosis',
    'atom': 'cosmos',
    'akash': "akash-network",
    'ust': 'terra-luna',
}

chainAPIs = {
    "dig": 'https://api-1-dig.notional.ventures/cosmos/gov/v1beta1/proposals',
    'juno': 'https://lcd-juno.itastakers.com/cosmos/gov/v1beta1/proposals',
    'huahua': 'https://api.chihuahua.wtf/cosmos/gov/v1beta1/proposals',
    'osmo': 'https://osmo.api.ping.pub/cosmos/gov/v1beta1/proposals',
    'atom': 'https://cosmos.api.ping.pub/cosmos/gov/v1beta1/proposals',
    'akash': 'https://akash.api.ping.pub/cosmos/gov/v1beta1/proposals',
    'ust': 'https://fcd.terra.dev/cosmos/gov/v1beta1/proposals',
}


def getSecrets():
    with open("secrets.prop", "r") as f:
        secrets = f.read().splitlines()
        f.close()
    return secrets

secrets = getSecrets()
APIKEY = secrets[0]
APIKEYSECRET = secrets[1]
ACCESS_TOKEN = secrets[2]
ACCESS_TOKEN_SECRET = secrets[3]


def tweet(chainSymbol, propID, title, voteEndTime=""):
    # Authenticate to Twitter
    auth = tweepy.OAuth1UserHandler(APIKEY, APIKEYSECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    api = tweepy.API(auth, wait_on_rate_limit=True)

    # message = f"{title}. Vote by {votePeriodEnd} - https://ping.pub/{chainSymbol}/gov/{propID}"
    message = f"${str(chainSymbol).upper()} | Proposal #{propID} | VOTING_PERIOD | {title} | https://ping.pub/{pingPubName[chainSymbol]}/gov/{propID}"
    print(message)

    if IN_PRODUCTION:
        try:
            tweet = api.update_status(message)
            print(f"Tweet sent for {tweet.id}: {message}")
            # api.update_status(in_reply_to_status_id=tweet.id, status=f"Voting Ends: ")
        except:
            print("Tweet failed due to being duplicate")
        


def betterTimeFormat(ISO8061):
    return ISO8061.replace("T", " ").split(".")[0]

def getAllProposals(chainSymbol):
    response = requests.get(chainAPIs[chainSymbol], headers={'accept': 'application/json', 'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'})
    props = response.json()['proposals']
    return props

def getNewestProposalID(proposalsJSON) -> int:
    return int(proposalsJSON[-1]['proposal_id'])


def checkIfNewestProposalIDIsGreaterThanLastTweet(chainSymbol):
    # and that it is currently in voting period


    # check if file exist
    if not os.path.exists(f"{chainSymbol}.txt"):
        with open(f"{chainSymbol}.txt", "w") as f:
            f.write("0")
            f.close()

    # open text file
    with open(f"{chainSymbol}.txt", "r") as f:
        lastPropID = int(f.read())
        print(f"{chainSymbol} Last prop ID tweeted: {lastPropID}")

    props = getAllProposals(chainSymbol)

    # get newest proposal ID, may not be in voting period FYI.

    for prop in props[lastPropID:getNewestProposalID(props)]:
        # if it is "PROPOSAL_STATUS_VOTING_PERIOD" and is greater than last prop ID
        current_prop_id = int(prop['proposal_id'])
        if prop['status'] == "PROPOSAL_STATUS_VOTING_PERIOD" and current_prop_id > lastPropID:            
            print(f"Newest prop ID {current_prop_id} is greater than last prop ID {lastPropID}")

            # save newest prop ID to file
            with open(f"{chainSymbol}.txt", "w") as f:
                f.write(str(current_prop_id))
                f.close()
                
            tweet(
                chainSymbol=chainSymbol,
                propID=prop['proposal_id'], 
                title=prop['content']['title'], 
                # votePeriodEnd=betterTimeFormat(prop['voting_end_time'])
            )


def runChecks():
    for chain in chainAPIs.keys():
        # _id = getNewestProposalID(chain)
        # print(f"{chain}: {_id}")
        checkIfNewestProposalIDIsGreaterThanLastTweet(chain)

if IN_PRODUCTION:
    print("CosmosGovProps Bot now running in production.")
else:
    print("CosmosGovProps Bot now running in testing mode.")

if IN_PRODUCTION:    
    runChecks()
    schedule.every(5).minutes.do(runChecks)
    while True:
        schedule.run_pending()
        time.sleep(60)
else:
    schedule.every(1).seconds.do(runChecks)
    while True:
        schedule.run_pending()
        time.sleep(1)


# Old code:
    # tweet(
    #     title=f"${chainSymbol} | Proposal #{prop['proposal_id']} | {prop['content']['title']}", 
    #     desc=prop['content']['description'],
    #     votePeriodEnd=betterTimeFormat(prop['voting_end_time'])
    # )

    # print out details of proposal
    # for i in range(0, len(desc), 280):
    #     tweet =  api.update_status(in_reply_to_status_id=tweet.id, status=desc[i:i+280])
    # print(desc[i:i+140])

    # api.update_status(in_reply_to_status_id=tweet.id, status=f"https://ping.pub/{chainSymbol}/gov/{propID}")


    ## get json keys
    # for key in props:
    #     for k in key:
    #         print(f"{k}", end=", ")


# def getProposals(chainSymbol, id):
#     # Get all proposals (past and future) from chain 
#     # response = requests.get(chainAPIs[chainSymbol], headers={'accept': 'application/json',})
#     # props = response.json()['proposals']
#     # print(props)
#     # for prop in props:
#     #     # if prop['proposal_id'] in ["1", "2", "3", '4']:
#     #     #     continue
#         # tweet(
#         #     chainSymbol=chainSymbol,
#         #     propID=prop['proposal_id'], 
#         #     title=f"${str(chainSymbol).upper()} | Proposal #{prop['proposal_id']} | {prop['content']['title']}", 
#         #     votePeriodEnd=betterTimeFormat(prop['voting_end_time'])
#         # )
#     #     break
#     pass