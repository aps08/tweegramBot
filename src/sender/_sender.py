import logging
import os
import time
from datetime import datetime, timedelta, timezone
from typing import Tuple

from telethon.sync import TelegramClient


class TelegramOperation:
    """
    Source operations
    command_check : default value False, pass True if you
                   want to use commands.
    """

    def __init__(self, command_check: bool):
        self.__client = TelegramClient("tweegramBot", os.environ.get("API_ID"), os.environ.get("API_HASH")).start()
        self.check = command_check
        self.s_error = False
        self.__logger = logging.getLogger("tweegramBot")
        self.__logger.info("sender module is initialized.")

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
            self.__logger.info("running %s", self.command_check.__name__)
            for _, value in enumerate(telegram_data):
                message = value.get("message", "")
                if message:
                    message = message.strip()
                    if message.startswith("@notice"):
                        pass
                        self.__logger.info("Ignoring notice.")
                    elif message.startswith("@add") or message.startswith("@remove"):
                        filtered_commands.append(message)
                    else:
                        filtered_message.append(value)
                else:
                    filtered_message.append(value)
            self.__logger.info("Filtering commands and messages completed.")
        except Exception as comm_err:
            self.__logger.error("Error in %s %s", self.command_check.__name__, comm_err)
            self.s_error = True
            raise comm_err
        return filtered_commands, filtered_message

    def get_messages(
        self, text: bool = True, image: bool = True, video: bool = True, gif: bool = True
    ) -> Tuple[list, list]:
        """
        Gets all the messages which are posted
        after a perticular interval of time.
        You can also pass the keyword in order to
        filter messages.
            text : default value True.
            image : default value True.
            video : default value True.
            gif : default value True.
        """
        try:
            self.__logger.info("running %s", self.get_messages.__name__)
            fetched_data = []
            date_time = datetime.now(timezone.utc) - timedelta(hours=1.0)
            messages = self.__client.iter_messages(entity=os.environ.get("ENTITY"), offset_date=date_time, reverse=True)
            self.__logger.info("Getting messages from telegram from past 1 hour.")
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
            self.__logger.error("Error in %s %s", self.get_messages.__name__, get_message_err)
            self.s_error = True
            raise get_message_err
        return commands, message

    def send_message(self, text: str) -> bool:
        """
        Sends message to the owner if the twitter
        account user is trying to add doesn't exists.
        argument:
            text: Default value "",string message to be sent
                 to the owner.
        return:
            sent: True if message sent successfully.
        """
        try:
            self.__logger.info("running %s", self.send_message.__name__)
            sent = False
            if text:
                self.__client.send_message(entity="me", message=text)
                sent = True
                self.__logger.info("sent the text.")
        except Exception as send_message_err:
            self.__logger.error("Error in %s %s", self.send_message.__name__, send_message_err)
            self.s_error = True
            raise send_message_err
        return sent
