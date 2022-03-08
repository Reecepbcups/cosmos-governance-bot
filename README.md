# CosmosGovernanceProposalBot
A twitter + discord webhook bot to notify users of governance proposals when in voting period
https://twitter.com/CosmosGovNotifs

Discord notifications can be found in the ChandraStation Discord
https://discord.gg/2GwEehcTa4

# Current Notifications for:
## Major
ATOM, OSMO, JUNO, AKT, SECRET, TERRA, HUAHUA, STARS, CMDX, CRO, EVMOS, GRAVITY, INJ, IRIS, LUM, REGEN 

## Nicher
DIG, DVPN, KAVA, LIKE, XPRT, BCNA, BITSONG, BOSTROM, CHEQD, PB, SIF, UMEE, Starname (iov), Band, FetchAI


# Configuration
1) Update secrets.json to your own values. 
*If you do not plan on using one of the bots, you do not need to fill out the values.*

2) If you want to allow all tickers to be announced, leave TICKERS_TO_ANNOUNCE as []

To specify tickers, add them in a list as `["dig","osmo","huahua"]` matching tickers in the twitterGovBot.py script chainIds*

3) Open the .py script and edit the following:

IN_PRODUCTION
DISCORD
TWITTER

USE_PYTHON_RUNNABLE 
*if true, run the script in a screen such as `screen -S bot python3 twitterGovernanceBot.py`*
*if false, use a cronjob to auto run it when you want, use https://crontab.guru/examples.html for help, must cd to directory first*

LOG_RUNS
*Just adds logs.txt for when the script is run to ensure success*
