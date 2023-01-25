"""
All telegram operations are performed here.
"""

import os
import re
from datetime import datetime, timedelta, timezone
from typing import Tuple

from dotenv import load_dotenv
from telethon.sync import TelegramClient

load_dotenv()


class TelegramOps:
    """
    Source operations
    """

    def __init__(self, API_ID: str, API_HASH: str):
        """constructor"""
        self.__client = TelegramClient("aps08", API_ID, API_HASH).start()

    def get_messages(self) -> Tuple[list, list]:
        """
        Gets all the messages which are posted
        after a perticular interval of time.
        """
        fetched_data = []
        command_message = []
        try:
            date_time = datetime.now(timezone.utc) - timedelta(hours=1.0)
            for message in self.__client.iter_messages(
                entity="pytweegram", offset_date=date_time, reverse=True
            ):
                current_timestamp = datetime.now().strftime("%Y%d%m_%H%M%S_%f")
                export = "media/" + current_timestamp
                fetched_message, image_path = None, None
                if (message.photo and message.message) and ("@notice" not in message.message):
                    image_path = self.__client.download_media(message, export)
                elif message.photo and not message.message:
                    image_path = self.__client.download_media(message, export)
                elif (message.message and not message.photo) and ("@notice" not in message.message):
                    text = message.message
                    text = text.strip()
                    if re.match("@add", text, re.IGNORECASE) or re.match(
                        "@remove", text, re.IGNORECASE
                    ):
                        command_message.append(text)
                    else:
                        fetched_message = text
                else:
                    print("Notice chat/Not text or image.")
                if image_path and "\\" in image_path:
                    image_path = image_path.replace("\\", "/")
                if fetched_message or image_path:
                    fetched_data.append({"message": fetched_message, "image": image_path})
        except Exception as get_message_err:
            raise get_message_err
        return fetched_data, command_message

    def send_message(self, text: str):
        """
        Sends message to the owner if the twitter
        account user is trying to add doesn't exists.
        """
        try:
            self.__client.send_message(entity="me", message=text)
        except Exception as send_message_err:
            raise send_message_err


TelegramOps = TelegramOps(os.environ.get("API_ID"), os.environ.get("API_HASH"))
print(TelegramOps.get_messages())
