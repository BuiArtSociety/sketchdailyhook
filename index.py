# Imports
import asyncio
import asyncpg

import datetime
import time

from dhooks import Webhook

from tools import default

# Getting the config file for webhook links
config = default.get("config.json")

# Print that it's working
print(f"{config.name} by {config.owner} running!")


# Making a function for starting
async def run():
    # Naming the database and logging in
    credentials = {
        "user": config.dbname,
        "password": config.dbpass,
        "database": config.database,
        "host": "127.0.0.1",
    }
    db = await asyncpg.create_pool(**credentials)
    # Make the table if it's not here
    await db.execute(
        "CREATE TABLE IF NOT EXISTS sketchdaily(code int, artist varchar, idea varchar);"
    )
    # Cgecj fir the time
    while True:
        now = datetime.datetime.utcnow()
        dayMonth = datetime.date.today()
        # If the time is 3 PM UTC and if it is
        if now.hour is 15 and now.minute is 00:
            # Get a random entry
            row = await db.fetchrow(
                "SELECT * FROM sketchdaily ORDER BY RANDOM() LIMIT 1;"
            )
            if row is None:
                # If there are no entries print so
                return print("There are no suggestions...")
            # Else, say it's ready and start the process
            print("True, sending webhook message")
            # Define the webhook
            hook = Webhook(config.webhookurl, is_async=True)
            hook2 = Webhook(config.webhook2, is_async=True)
            hook3 = Webhook(config.webhook3, is_async=True)
            # Send webhook messages to the two servers
            await hook.send(
                f"<@&509164409604669450>\n\nThe prompt for {dayMonth.day}/{dayMonth.month}/{dayMonth.year} is:\n\n**{row['idea']}**\n\nIt was suggested by **{row['artist']}**\n\nPlease post your submission below this line!\n\n==================="
            )
            await hook2.send(
                f"Want some inspiration to draw or write?\nToday's prompt is:\n\n**{row['idea']}**\nSuggested by **{row['artist']}**\n\nTry out making something using this!!\nPost your submissions in this channel when done!"
            )
            await hook3.send(f"Want some inspiration or ideas to draw and/or write?\nToday's prompt is:\n\n**{row['idea']}**\nSuggested by **{row['artist']}**\n\nTry making something out with the prompt. Post your submission in either <#338060584291532821> and/or <#441768190901485578> when done!")
            # End it
            await hook.close()
            await hook2.close()
            await hook3.close()
            # FInd the entry, delete and sleep for a minuite
            sketchcode = row["code"]
            query = "DELETE FROM sketchdaily WHERE code=$1;"
            await db.execute(query, sketchcode)
            time.sleep(60)
        else:
            # Else, check again in 15 seconds
            time.sleep(15)


# The async loop begins
loop = asyncio.get_event_loop()
loop.run_until_complete(run())


