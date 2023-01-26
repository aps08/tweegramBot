"""
All twitter operations are performed here.
"""
import os

from dotenv import load_dotenv

load_dotenv()


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


import tweepy

client = tweepy.Client(
    consumer_key=os.environ.get("API_ID"),
    consumer_secret=os.environ.get("API_SECRET"),
    access_token=os.environ.get("ACCESS_TOKEN"),
    access_token_secret=os.environ.get("ACCESS_TOKEN_SECRET"),
)
auth = tweepy.OAuthHandler(
    consumer_key=os.environ.get("API_ID"),
    consumer_secret=os.environ.get("API_SECRET"),
    access_token=os.environ.get("ACCESS_TOKEN"),
    access_token_secret=os.environ.get("ACCESS_TOKEN_SECRET"),
)
# twitter_api = tweepy.API(auth)
# data = twitter_api.update_status("bot")
data = client.get_all_tweets_count(query="covid")

print(data)
