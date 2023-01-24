import os
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv
from telethon.sync import TelegramClient

load_dotenv()

# with TelegramClient("aps08", os.environ.get("API_ID"), os.environ.get("API_HASH")) as client:
client = TelegramClient("aps08", os.environ.get("API_ID"), os.environ.get("API_HASH"))
client.start()
entity = client.get_entity("altaps080")
client.send_message(entity=entity, message="Message")
