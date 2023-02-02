import datetime
import os
import re
import shutil

from receiver import receiver
from sender import sender
from store import file

# sender = sender(command_check=True)
receiver = receiver(link_fc=True)
file = file()
# commands, messages = sender.get_messages()
for command in ["@add aps08", "@remove aps08"]:
    if command.startswith("@add"):
        user_name = command.split(" ")[-1]
        user_id = receiver.get_user_id(user_name=user_name)
        if user_id:
            token = file.create_token()
            added = file.add_user(user_name, token, user_id)
            if added:
                tweet_string = f"""
                Thank you for joining us @{user_name}.
                You have been added to our list with
                #{token}. Tag us with this token as
                hashtag.
                """
                receiver.convert_to_tweet([{"message": tweet_string, "image": None}])
                telegram_message = f"{user_name} added to list."
        else:
            telegram_message = f"{user_name} not found on twitter, please check again."
    if command.startswith("@remove"):
        user_name = command.split(" ")[-1]
        exists, active = file.check_user_exists(user_name)
        if exists:
            if active:
                file.remove_user(user_name)
                telegram_message = f"{user_name} removed to list."
            else:
                telegram_message = f"{user_name} already removed from the list."
    sender.send_message(telegram_message)
