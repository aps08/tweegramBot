"""
All telegram operations are performed here.
"""


import os
from datetime import datetime, timedelta, timezone
from typing import Tuple

from telethon.sync import TelegramClient


class TelegramOperation:
    """
    Source operations
    command_check (bool): default value False, pass true if you
                   want to use commands.
    """

    def __init__(self, command_check: bool = False):
        self.__client = TelegramClient(
            "aps08", os.environ.get("API_ID"), os.environ.get("API_HASH")
        ).start()
        self.__check = command_check

    def command_check(self, telegram_data: list) -> Tuple[list, list]:
        """
        Iterate through the data and check the commands
        argument:
            telegram_data: list of dictionary
        return:
            filtered_commands: list of commands
            filtered_message: list of dictionary of message
        """
        filtered_commands = []
        filtered_message = []
        try:
            for index, value in enumerate(telegram_data):
                if value["message"]:
                    message = value["message"].strip()
                    if message.startswith("@notice"):
                        print("Ignoring message as it's a notice")
                    elif message.startswith("@add") or message.startswith("@remove"):
                        filtered_commands.append(message)
                    else:
                        filtered_message.append(value)
                else:
                    filtered_message.append(value)
        except Exception as comm_err:
            raise comm_err
        return filtered_commands, filtered_message

    def get_messages(self) -> Tuple[list, list]:
        """
        Gets all the messages which are posted
        after a perticular interval of time.
        """
        try:
            fetched_data = []
            date_time = datetime.now(timezone.utc) - timedelta(days=1.0)
            for message in self.__client.iter_messages(
                entity="pytweegram", offset_date=date_time, reverse=True
            ):
                current_timestamp = datetime.now().strftime("%Y%d%m_%H%M%S_%f")
                export = "media/" + current_timestamp
                fetched_message, image_path = None, None
                if message.photo and message.message:
                    image_path = self.__client.download_media(message, export)
                    fetched_message = message.message
                elif message.photo and not message.message:
                    image_path = self.__client.download_media(message, export)
                elif message.message and not message.photo:
                    fetched_message = message.message
                else:
                    print("Not text or image.")
                if image_path and "\\" in image_path:
                    image_path = image_path.replace("\\", "/")
                if fetched_message or image_path:
                    fetched_data.append({"message": fetched_message, "image": image_path})
            if self.__check:
                commands, message = self.__command_check(fetched_data)
            else:
                commands, message = [], fetched_data
        except Exception as get_message_err:
            raise get_message_err
        return commands, message

    def send_message(self, text: str):
        """
        Sends message to the owner if the twitter
        account user is trying to add doesn't exists.
        argument:
            text: string message to be sent to the owner.
        """
        try:
            self.__client.send_message(entity="me", message=text)
        except Exception as send_message_err:
            raise send_message_err
