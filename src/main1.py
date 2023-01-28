import os
import re
import shutil

from receiver import receiver
from sender import sender

current_dir = os.getcwd()
path = os.path.join(current_dir, "media")
shutil.rmtree(path)
receiver = receiver(True)
TelegramOps = sender(True)
command_list, message_list = TelegramOps.get_messages()
receiver.convert_to_tweet()
