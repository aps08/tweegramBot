import os

import tweepy
from dotenv import load_dotenv
from tweepy.api import API
from tweepy.client import Client

load_dotenv()


class Creator:
    """
    Creates required objects
    """

    def get_client(self) -> Client:
        """
        Creates and return client object
        """
        try:
            client = tweepy.Client(
                bearer_token=os.environ.get("BEARER_TOKEN"),
                consumer_key=os.environ.get("API_KEY"),
                consumer_secret=os.environ.get("API_SECRET"),
                access_token=os.environ.get("ACCESS_TOKEN"),
                access_token_secret=os.environ.get("ACCESS_TOKEN_SECRET"),
            )
        except Exception as client_obj_err:
            raise client_obj_err
        return client

    def get_oauth(self) -> API:
        """
        Creates and return oauth api handler
        """
        try:
            auth = tweepy.OAuthHandler(
                consumer_key=os.environ.get("API_KEY"),
                consumer_secret=os.environ.get("API_SECRET"),
                access_token=os.environ.get("ACCESS_TOKEN"),
                access_token_secret=os.environ.get("ACCESS_TOKEN_SECRET"),
            )
            twitter_api = tweepy.API(auth)
        except Exception as oauth_obj_err:
            raise oauth_obj_err
        return twitter_api
