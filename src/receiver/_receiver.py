"""
All twitter operations are performed here
without command features.
"""
import os

import tweepy
from dotenv import load_dotenv

from receiver._access import Creator

load_dotenv()


class TwitterOperations(Creator):
    """
    Destination operation.
    """

    def __init__(self, link_fc: bool = False):
        """constructor"""
        Creator.__init__(self)
        self.__link_fc = link_fc

    def __reply_with_link(self):
        """
        reply with link in first comment
        """
        try:
            pass
        except Exception as reply_lfc_err:
            raise reply_lfc_err

    def convert_to_tweet(self, items: list) -> None:
        """
        Iterate list items and converts
        them into tweet.
        """
        try:
            client = self.get_client()
            oauth_api = self.get_oauth()
            for item in items:
                message, image = item["message"], item["image"]
                if message and image:
                    media = oauth_api.media_upload(image)
                    res = client.create_tweet(text=message, media_ids=[media.media_id])
                elif message and not image:
                    res = client.create_tweet(text=message)
                elif image and not message:
                    media = oauth_api.media_upload(image)
                    res = client.create_tweet(text=message, media_ids=[media.media_id])
        except Exception as send_tweet_err:
            raise send_tweet_err
