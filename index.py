import time
import datetime
from discord_webhook import DiscordWebhook
from tools import default

config = default.get("config.json")

print(f"{config.name} by lyricalpaws running!")

while True:
    now = datetime.datetime.utcnow()

    if now.hour is 22 and now.minute is 41:
        print('True')
        webhook = DiscordWebhook(url=f'{config.webhookurl}', content='Webhook Message')
        webhook.execute()
        time.sleep(60)
    else:
        print('False')
        time.sleep(15)
