import time
import datetime
import asyncpg
import asyncio
from discord_webhook import DiscordWebhook
from tools import default

config = default.get("config.json")

print(f"{config.name} by {config.owner} running!")


async def run():
    credentials = {"user": config.dbname, "password": config.dbpass, "database": config.database, "host": "127.0.0.1"}
    db = await asyncpg.create_pool(**credentials)
    await db.execute("CREATE TABLE IF NOT EXISTS sketchdaily(artist varchar, idea varchar);")

loop = asyncio.get_event_loop()
loop.run_until_complete(run())

while True:
    now = datetime.datetime.utcnow()

    if now.hour is 00 and now.minute is 29:
        print('True')
        webhook = DiscordWebhook(url=f'{config.webhookurl}', content='Webhook Message')
        webhook.execute()
        time.sleep(60)
    else:
        print('False')
        time.sleep(15)
