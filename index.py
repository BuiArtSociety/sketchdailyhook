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
    await db.execute("CREATE TABLE IF NOT EXISTS sketchdaily(code int, artist varchar, idea varchar);")

    while True:
        now = datetime.datetime.utcnow()
        dayandmonth = datetime.date.today()
        if now.hour is 23 and now.minute is 0:
            row = await db.fetchrow("SELECT * FROM sketchdaily ORDER BY RANDOM() LIMIT 1;")
            if row is None:
                return print("There are no suggestions...")
            print('True, sending webhook message')
            webhook = DiscordWebhook(url=f'{config.webhookurl}', content=f"<@&509164409604669450>\n\nThe prompt for {dayandmonth.day}/{dayandmonth.month}/{dayandmonth.year} is:\n\n**{row['idea']}**\n\nIt was suggested by **{row['artist']}**\n\nPlease post your submission below this line!\n\n===================")
            webhook.execute()
            sketchcode = row['code']
            query = "DELETE FROM sketchdaily WHERE code=$1;"
            await db.execute(query, sketchcode)
            time.sleep(60)
        else:
            time.sleep(15)


loop = asyncio.get_event_loop()
loop.run_until_complete(run())
