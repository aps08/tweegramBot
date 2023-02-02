"""
All twitter operations are performed here
without command features.
"""
import os
import shutil
from datetime import datetime
from typing import Tuple

from _access import Creator
from dotenv import load_dotenv
from validator_collection import checkers

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

    def remove_media(self) -> bool:
        """
        Fully remove the media folder.
        removed: True if folder is removed.
        """
        try:
            removed = False
            current_dir = os.getcwd()
            path = os.path.join(current_dir, "media")
            if os.path.exists(path):
                shutil.rmtree(path)
                removed = True
        except Exception as del_err:
            raise del_err
        return removed

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
                            ValueError("Message should only contain URL, when __link_fc is True")
                    else:
                        media = self.__oauth_api.media_upload(image)
                        res = self.__client.create_tweet(text=message, media_ids=[media.media_id])
                elif message and not image:
                    res = self.__client.create_tweet(text=message)
                elif image and not message:
                    media = self.__oauth_api.media_upload(image)
                    res = self.__client.create_tweet(text=default_message, media_ids=[media.media_id])
            self.__remove_media()
        except Exception as send_tweet_err:
            raise send_tweet_err

    def get_user_id(self, user_name: str) -> int:
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

    def extract_token(self, tweet_text: str) -> str:
        """
        Extracts the token from teh text.
        return:
            token: the token for verification
        """
        try:
            pass
        except Exception as token_err:
            raise token_err

    def tweet_info(self, tweet_id: int) -> Tuple[int, str, str]:
        """
        Get information about a tweet id
        return:
            author_id: id of user whose has written the tweet
            token: token used in the tweet
            username: twitter username of the user
        """
        try:
            author_id, token, username = None, None, None
            tweets_data = self.__client.get_tweet(tweet_id, expansions=["author_id"])
            print(tweets_data)
        except Exception as tweet_info_err:
            raise tweet_info_err
        return author_id, token, username

    def get_mentioned_tweets(self, user_id: int):
        current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        tweets_data = self.__client.get_users_mentions(
            id=user_id, max_results=100, start_time="2023-01-03T18:17:44Z", expansions=["in_reply_to_user_id"]
        )
        for item in tweets_data.data:
            print(dict(item))

    def re_tweet(self, tweet_id: int):
        """
        Retweet the
        """


# tech_referrals
TwitterOperations = TwitterOperations()
# user_id = TwitterOperations.get_user_id(user_name="tech_referrals")
# TwitterOperations.get_mentioned_tweets(user_id)
TwitterOperations.tweet_info(1616119474108891136)
