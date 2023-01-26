import os

from receiver import receiver
from sender import sender

receiver = receiver()
TelegramOps = sender(True)
command_list, message_list = TelegramOps.get_messages()
print(command_list, message_list)
# receiver.convert_to_tweet(message_list)
