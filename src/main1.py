import datetime
import os
import re
import shutil

from receiver import receiver
from sender import sender

# sender = sender(command_check=True)
receiver = receiver(link_fc=True)
# commands, messages = sender.get_messages()
for command in ["@add aps08", "@remove aps08"]:
    if command.startswith("@add"):
        user_name = command.split(" ")[-1]
        user_id = receiver.user_info(user_name=user_name)
        if user_id:
            token = None
            # add user in the json
            tweet_string = f"""
            Thank you for joining us @{user_name}.
            You have been added to our list with
            #GTR_{token}. Use the token as a hashtag.
            """
            receiver.convert_to_tweet([{"message": tweet_string, "image": None}])
            # create token
            # create tweet
    if command.startswith("@remove"):
        user_name = command.split(" ")[-1]
        # check if username exists in the json
        exists = False
        if exists:
            # change the active flag to false
            print("A")
