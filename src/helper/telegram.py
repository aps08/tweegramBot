"""
This module is responsible for getting 
text and media from telegram.
"""

from datetime import datetime, timedelta, timezone

from telethon.sync import TelegramClient


class RecieveMessage:

    __slots__ = "__id", "__hash", "__group"

    def __init__(self, id: str, hash: str, group: str) -> None:
        """Constructor"""
        self.__id = id
        self.__hash = hash
        self.__group = group

    def download_media(self) -> dict:
        """
        Download text and media and returns a
        dictionary containing media path and text.
        """
        date_time = datetime.now(timezone.utc) - timedelta(days=2.0)
        items = {}
        with TelegramClient("aps08", self.__id, self.__hash) as client:
            media_count = 0
            for message in client.iter_messages(self.__group):
                export_path = f"src\\media\\{media_count}"
                if message.date > date_time:
                    temp_dict = {}
                    if message.photo:
                        path = client.download_media(message, export_path)
                        temp_dict["media_path"] = path
                        temp_dict["message"] = message.text
                    else:
                        temp_dict["message"] = message.text
                    items[media_count] = temp_dict
                    media_count += 1
        return items


if __name__ == "__main__":
    api_id = "9439839"
    api_hash = "7d738c894a2a3ea1e6835a84c7220b53"
    group_name = "coder_jain_dev_support"
