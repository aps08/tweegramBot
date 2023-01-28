"""
All twitter operations are performed here
without command features.
"""
import os
import re
import shutil

import tweepy
from dotenv import load_dotenv
from validator_collection import checkers

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

    def __remove_media(self) -> None:
        """
        Fully remove the media folder.
        """
        try:
            current_dir = os.getcwd()
            path = os.path.join(current_dir, "media")
            shutil.rmtree(path)
        except Exception as del_err:
            raise del_err

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
                    if self.__link_fc:
                        valid = checkers.is_url(message)
                        if valid:
                            media = oauth_api.media_upload(image)
                            # Here you can provide some caption to the image or any message according to your use case.
                            message = ""
                            res = client.create_tweet(text="", media_ids=[media.media_id])
                            id = list(res)[0]["id"]
                            res = client.create_tweet(text=message, in_reply_to_tweet_id=id)
                        else:
                            ValueError("Only pass URL in message, when __link_fc is True")
                    else:
                        media = oauth_api.media_upload(image)
                        res = client.create_tweet(text=message, media_ids=[media.media_id])
                elif message and not image:
                    res = client.create_tweet(text=message)
                elif image and not message:
                    media = oauth_api.media_upload(image)
                    # Here you can provide some caption to the image or any message according to your use case.
                    res = client.create_tweet(text=message, media_ids=[media.media_id])
            self.__remove_media()
        except Exception as send_tweet_err:
            raise send_tweet_err
