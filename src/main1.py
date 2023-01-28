import datetime
import os
import re
import shutil

from receiver import receiver
from sender import sender

receiver = receiver(True)
# TelegramOps = sender(True)
# command_list, message_list = TelegramOps.get_messages()
id = receiver.user_info("")
receiver.get_tweets(id)
n = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=5.0)
n.isoformat()
print(n)
