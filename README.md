# Auto Covid Bot

Automatically fill out the [NYC DOE health screening form](https://healthscreening.schools.nyc/) by registering with a discord bot

School code can be found on https://schoolsearch.schools.nyc/

Use by joining [this discord](https://discord.gg/6G4kNjqpfb)

Credits to https://github.com/hair for https://github.com/hair/autoCovid, the base for this bot

## Self hosting
Not recommended, I have no intention of making this any easier in the near future, but it's doable. Also, everything will likely break in the future when I inevitable decide that the current code is spaghetti.

Replace `916896832737648710` in `guild_ids` with your guild's id

Dependencies:
```sh
pip install git+https://github.com/Pycord-Development/pycord
pip install asyncio
pip install aiohttp
```


Have cron run cronscript.py every day at 6 am
```cron
0 5 * * * python3 /path/to/cronscript.py
```

Run bot:
```sh
TOKEN="<token>" python main.py
```

By using you agree to the [license](https://github.com/cleonyc/autocovidbot/blob/main/LICENSE)