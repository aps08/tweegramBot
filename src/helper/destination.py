"""
All twitter operations are performed here.
"""


class TwitterOps:
    """
    Destination Operations
    """

    def __init__(self):
        """construtor"""
        pass

    def user_lookup(self, username: str) -> bool:
        """
        returns True if username exists on Twitter
        """
        exists = False
        try:
            pass
        except Exception as loopup_err:
            raise loopup_err
        return exists

    def send_dm(self, token: str) -> None:
        """
        send direct message with token
        to be used for tweets.
        """
        try:
            pass
        except Exception as dm_err:
            raise dm_err

    def tweet(self) -> None:
        pass
