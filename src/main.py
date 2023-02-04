import receiver
import sender
import store


class TweegramBot(receiver, sender, store):
    def __init__(self) -> None:
        super().__init__()
