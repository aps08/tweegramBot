from receiver import receiver
from sender import sender
from store import file


class TweegramBot(receiver, sender, file):
    def __init__(self, username: str, link_fc: bool = False, retweet_text: str = "Retweet for better reach."):
        file.__init__(self)
        sender.__init__(self)
        receiver.__init__(self)
