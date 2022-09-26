from datetime import datetime, timedelta, timezone

from telethon.sync import TelegramClient

api_id = "9439839"
api_hash = "7d738c894a2a3ea1e6835a84c7220b53"
group_name = "coder_jain_dev_support"
date_time = datetime.now(timezone.utc) - timedelta(days=2.0)
dic = {}
with TelegramClient("aps08", api_id, api_hash) as client:
    media_count = 0
    for message in client.iter_messages(group_name):
        export_path = f"src\\media\\{media_count}"
        if message.date > date_time:
            temp_dict = {}
            if message.photo:
                path = client.download_media(message, export_path)
                temp_dict["media_path"] = path
                temp_dict["message"] = message.text
            else:
                temp_dict["message"] = message.text
            dic[media_count] = temp_dict
            media_count += 1
print(dic)
