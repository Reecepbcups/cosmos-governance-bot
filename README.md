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

2) If you want to allow all tickers to be announced, leave TICKERS_TO_ANNOUNCE as `[]`
<br>To specify tickers, add them in a list as `["dig","osmo","huahua"]` matching tickers in the GovBot.py script chainIds*

3) Open the .py script and edit the following:

IN_PRODUCTION<br>
DISCORD<br>
TWITTER<br>

USE_PYTHON_RUNNABLE 
*if true, run the script in a screen such as `screen -S bot python3 GovBot.py`*<br>
*if false, use a cronjob to auto run it when you want, use https://crontab.guru/examples.html for help, must cd to directory first*<br>

such as: `*/30 * * * * cd /root/CosmosBot && python3 GovBot.py`<br>

LOG_RUNS
*Just adds logs.txt for when the script is run to ensure success*
</br></br>
## Discord Threads
For threads, you must set `DISCORD = True` in GovBot.py. Within your discord client you will need 2 things:<br>
- The Channel_ID *(right click the channel and it should be at the very bottom. If not, settings > Advanced > Developer Mode)*<br>
- Guild ID (right click the server icon, and copy ID)<br>
NOTE: You must use the same channel_id as the webhook is generated on
</br></br>
Next you need to set your `THREAD_ARCHIVE_MINUTES`. There are 4 values you can do: `60, 1440, 4320, 10080`</br>
- By default level 0 servers only have 60 and 1440 (24hours). To get access to other values, you have to increase your server boost.
</br></br>
Finally you must setup a bot application, HOWEVER it is not actually run like a normal bot. 
We just pass it through discords endpoints & simulate it being on. So no hassle :)
- https://discord.com/developers/applications
- New Application in the top (Then name it, create)
- On the left, click "Bot"
- On the right, "Add Bot", then "Yes Do It"
</br></br>
- Click on "Reset Token' to get the Bots Token, then "Yes Do It" (You may be required to enter a 2fa code here)
- *Example Token: OTUyMDgwOTQ5NzcwODUwMzY1.Yiw0ew.8Fsxi4I4IMgmAICyh_HdsIXL_jo*
- Paste this token into the secret.json file under "DISCORD_THREADS" -> "BOT_TOKEN"
</br></br>
- Now back on the browser, click on "OAuth2" on the left
- Under the "URL Generator" tab, in scopes select "bot" (center, middle)
- In Bot Permissions, select the following:
![bot-values](https://user-images.githubusercontent.com/31943163/158006570-a48077f7-41fd-4440-80bf-67fe1bf516b8.png)

- Then at the bottom you should have a generated URL, copy this into your browser & invite it to the server
