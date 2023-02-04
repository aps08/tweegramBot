"""
All telegram operations are performed here.
"""


import os
import time
from datetime import datetime, timedelta, timezone
from typing import Tuple

from dotenv import load_dotenv
from telethon.sync import TelegramClient

load_dotenv()


class TelegramOperation:
    """
    Source operations
    command_check (bool): default value False, pass True if you
                   want to use commands.
    """

    def __init__(self, command_check: bool):
        self.__client = TelegramClient("aps", os.environ.get("API_ID"), os.environ.get("API_HASH")).start()
        self.check = command_check

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
            for _, value in enumerate(telegram_data):
                message = value.get("message", "")
                if message:
                    message = message.strip()
                    if message.startswith("@notice"):
                        pass
                    elif message.startswith("@add") or message.startswith("@remove"):
                        filtered_commands.append(message)
                    else:
                        filtered_message.append(value)
                else:
                    filtered_message.append(value)
        except Exception as comm_err:
            raise comm_err
        return filtered_commands, filtered_message

    def get_messages(
        self, text: bool = True, image: bool = False, video: bool = False, gif: bool = False
    ) -> Tuple[list, list]:
        """
        Gets all the messages which are posted
        after a perticular interval of time.
        You can also pass the keyword in order to
        filter messages.
        """
        try:
            fetched_data = []
            date_time = datetime.now(timezone.utc) - timedelta(hours=1.0)
            messages = self.__client.iter_messages(entity="pytweegram", offset_date=date_time, reverse=True)
            for message in messages:
                current_timestamp = datetime.now().strftime("%Y%d%m_%H%M%S_%f")
                export = "media/" + current_timestamp
                fetched_message, image_path = None, None
                if message.photo and message.message and all([text, image]):
                    image_path = self.__client.download_media(message, export)
                    fetched_message = message.message
                elif message.photo and not message.message and image:
                    image_path = self.__client.download_media(message, export)
                elif message.message and not message.photo and text:
                    fetched_message = message.message
                elif message.gif and gif:
                    image_path = self.__client.download_media(message, export)
                elif message.video and video:
                    image_path = self.__client.download_media(message, export)
                if image_path and "\\" in image_path:
                    image_path = image_path.replace("\\", "/")
                if fetched_message or image_path:
                    fetched_data.append({"message": fetched_message, "image": image_path})
            if self.check:
                commands, message = self.command_check(fetched_data)
            else:
                commands, message = [], fetched_data
        except Exception as get_message_err:
            raise get_message_err
        return commands, message

    def send_message(self, text: str = "", file: bool = False) -> bool:
        """
        Sends message to the owner if the twitter
        account user is trying to add doesn't exists.
        argument:
            text: Default value "",string message to be sent
                 to the owner.
            file: Default value False, True when you send
                log file.
        return:
            sent: True if message sent successfully.
        """
        try:
            sent = False
            if file:
                self.__client.send_file(entity="me", file="tweegram.log")
                sent = True
            else:
                self.__client.send_message(entity="me", message=text)
                sent = True
        except Exception as send_message_err:
            raise send_message_err
        return sent
