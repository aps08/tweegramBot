import receiver
import sender
import store


class TweegramBot(receiver, sender, store):
    def __init__(self, username: str, link_fc: bool = False, retweet_text: str = "Retweet for better reach."):
        store.__init__(self)
        sender.__init__(self)
        receiver.__init__(self)
