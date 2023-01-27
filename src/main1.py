import os
import re
import shutil

from receiver import receiver
from sender import sender

current_dir = os.getcwd()
path = os.path.join(current_dir, "media")
shutil.rmtree(path)
# receiver = receiver(True)
# TelegramOps = sender(True)
# command_list, message_list = TelegramOps.get_messages()
# print(command_list, message_list)
# receiver.convert_to_tweet(
#     [
#         {
#             "message": "blah blah https://www.linkedin.com/posts/sneprakash08_flipkart-is-hiring-on-instahyre-apply-now-activity-7024687227435712512-AsSz?utm_source=share&utm_medium=member_android after the link",
#             "image": None,
#         },
#         {"message": "https://aps08.medium.com", "image": "media/20232701_231730_147956.jpg"},
#     ]
# )
