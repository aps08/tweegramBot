"""
All twitter operations are performed here
without command features.
"""
import os
import re
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
                    in order to add link in first comment.
    """

    def __init__(self, username: str, link_fc: bool = False, retweet_text: str = "Retweet for better reach."):
        """constructor"""
        Creator.__init__(self)
        self.__link_fc = link_fc
        self.__client = self.get_client()
        self.__oauth_api = self.get_oauth()
        self.__username = username
        self.__retweet_text = retweet_text

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

    def get_user_id(self, user_name: str = "", author_id: int = 0) -> int | str:
        """
        Checks if user_name exists in twitter or not.
        argument:
            user_name: id to be checked against, default value ""
            author_id: username to be checked against, default value 0
        return:
            result: id or username as per input
        """
        try:
            result = None
            key = None
            if user_name:
                user_data = self.__client.get_user(username=user_name)
                key = "id"
            elif author_id:
                user_data = self.__client.get_user(id=author_id)
                key = "username"
            if user_data.data:
                user_data_dict = dict(user_data.data)
            result = user_data_dict.get(key, None)
        except Exception as user_err:
            raise user_err
        return result

    def tweet_info(self, tweet_id: int) -> dict:
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
            if tweets_data.data:
                tweet_data_dict = dict(tweets_data.data)
                author_id = tweet_data_dict.get("author_id", "")
                text = tweet_data_dict.get("text", "")
                hashlist = re.findall("#(\w+)", text)
                for hash in hashlist:
                    if hash.startswith("GTR"):
                        token = hash.split("_")[-1]
                username = self.get_user_id(author_id=author_id)
        except Exception as tweet_info_err:
            raise tweet_info_err
        return {"author_id": author_id, "token": token, "username": username}

    def get_mentioned_tweets(self) -> dict:
        """
        Gets tweet where the bot is mentioned.
        """
        try:
            tweet_data = dict()
            # date_time = datetime.now(timezone.utc) - timedelta(days=10.0)
            tweets_data = self.__client.search_recent_tweets(
                query=f"(hiring OR opening) (@{self.__username}) lang:en -is:reply -is:retweet",
                max_results=100,
                start_time="2023-01-27T18:17:44Z",
            )
            if tweets_data.data:
                for item in tweets_data.data:
                    item = dict(item)
                    tweet_id = item.get("id", 0)
                    data = {tweet_id: self.tweet_info(tweet_id)}
                    tweet_data.update(data)
        except Exception as mention_err:
            raise mention_err
        return tweet_data

    def re_tweet(self, tweet_id: int):
        """
        Retweet the
        """
        res = self.__client.create_tweet(text=self.__retweet_text, quote_tweet_id=tweet_id)
        print(res)


# tech_referrals
TwitterOperations = TwitterOperations()
# user_id = TwitterOperations.get_user_id(user_name="tech_referrals")
# print(TwitterOperations.get_mentioned_tweets())
# print(TwitterOperations.tweet_info(1621541525183430657))
TwitterOperations.re_tweet(1621541525183430657)
