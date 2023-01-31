"""
All twitter operations are performed here
without command features.
"""
import json
import os
import re
import shutil
from datetime import datetime

import tweepy
from dotenv import load_dotenv
from validator_collection import checkers

from receiver._access import Creator

load_dotenv()


class TwitterOperations(Creator):
    """
    Destination operation.
    link_fc (bool): default value False, change it to true,
                    in order to add links in first comment.
    """

    def __init__(self, link_fc: bool = False):
        """constructor"""
        Creator.__init__(self)
        self.__link_fc = link_fc
        self.__client = self.get_client()
        self.__oauth_api = self.get_oauth()

    def remove_media(self) -> None:
        """
        Fully remove the media folder.
        """
        try:
            current_dir = os.getcwd()
            path = os.path.join(current_dir, "media")
            if os.path.exists(path):
                shutil.rmtree(path)
        except Exception as del_err:
            raise del_err

    def convert_to_tweet(self, items: list, default_message: str = "") -> None:
        """
        Iterate list items and converts
        them into tweet.
        """
        try:
            for item in items:
                message, image = item["message"], item["image"]
                if message and image:
                    if self.__link_fc:
                        valid = checkers.is_url(message)
                        if valid:
                            media = self.__oauth_api.media_upload(image)
                            message = default_message
                            res = self.__client.create_tweet(text="", media_ids=[media.media_id])
                            id = list(res)[0]["id"]
                            res = self.__client.create_tweet(text=message, in_reply_to_tweet_id=id)
                        else:
                            ValueError("Only pass URL in message, when __link_fc is True")
                    else:
                        media = self.__oauth_api.media_upload(image)
                        res = self.__client.create_tweet(text=message, media_ids=[media.media_id])
                elif message and not image:
                    res = self.__client.create_tweet(text=message)
                elif image and not message:
                    media = self.__oauth_api.media_upload(image)
                    res = self.__client.create_tweet(
                        text=default_message, media_ids=[media.media_id]
                    )
            self.__remove_media()
        except Exception as send_tweet_err:
            raise send_tweet_err

    def user_info(self, user_name: str) -> int:
        """
        Checks if user_name exists in twitter or not.
        argument:
            user_name: user to be checked for
        return:
            id: id of the username
        """
        try:
            id = None
            user_data = self.__client.get_user(username=user_name)
            user_data = dict(user_data.data)
            id = user_data.get("id", None)
        except Exception as user_err:
            raise user_err
        return id

    def get_tweets(self, user_id: int):
        current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        tweets_data = self.__client.get_users_mentions(
            id=user_id, max_results=100, start_time="2023-01-03T18:17:44Z"
        )
        for item in tweets_data.data:
            i += 1
            print(i)
            print(dict(item))
