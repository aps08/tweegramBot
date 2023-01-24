"""
All telegram operations are performed here.
"""

import os
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv
from telethon.sync import TelegramClient

load_dotenv()


class TelegramSourceOps:
    """
    Source operations
    """

    def __init__(self, API_ID: str, API_HASH: str):
        """constructor"""
        self.__client = TelegramClient("aps08", API_ID, API_HASH).start()

    def __command_check(self):
        """
        Checks for all commands added.
        """
        try:
            pass
        except Exception as command_err:
            raise command_err

    def get_messages(self):
        """
        Gets all the messages which are posted
        after a perticular interval of time.
        """
        try:
            date_time = datetime.now(timezone.utc) - timedelta(hours=1.0)
            for message in self.__client.iter_messages("pytweegram", offset_date=date_time):
                print(message)
        except Exception as get_message_err:
            raise get_message_err

    def send_message(self, text: str):
        """
        Sends message to the owner if the twitter
        account user is trying to add doesn't exists.
        """
        try:
            pass
        except Exception as send_message_err:
            raise send_message_err


TelegramSourceOps = TelegramSourceOps(os.environ.get("API_ID"), os.environ.get("API_HASH"))
TelegramSourceOps.get_messages()
