"""
All twitter operations are performed here
without command features.
"""
import os
import re
import shutil
from datetime import datetime, timedelta, timezone

import tweepy
from dotenv import load_dotenv
from tweepy.api import API
from tweepy.client import Client
from validator_collection import checkers

load_dotenv()


class Creator:
    """
    Creates required objects.
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


class TwitterOperations(Creator):
    """
    Destination operation.
    first_comment (bool): default value False, change it to true,
                    in order to add link in first comment. When
                    this is True, and the text passed with the image
                    is a then it will be pasted in first comment.
    username (str): twitter username of the bot
    prefix (str): prefix to identify token from the hashtags
    retweet_text (str): Quote for retweet. Can't retweet with without
                    quote.
    """

    def __init__(self, username: str, first_comment: bool, prefix: str, retweet_text: str, only_img_mess: str):
        """constructor"""
        Creator.__init__(self)
        self.__client = self.get_client()
        self.__oauth_api = self.get_oauth()
        self.__first_comment = first_comment
        self.__username = username
        self.__retweet_text = retweet_text
        self.__prefic = prefix
        self.__only_img_mess = only_img_mess

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

    def convert_to_tweet(self, items: list) -> None:
        """
        Iterate list items and converts
        them into tweet.
        """
        try:
            for item in items:
                message, image = item.get("message", ""), item.get("image", "")
                if message and image:
                    if self.__first_comment:
                        valid = checkers.is_url(message)
                        if valid:
                            media = self.__oauth_api.media_upload(image)
                            res = self.__client.create_tweet(text=self.__only_img_mess, media_ids=[media.media_id])
                            id = list(res)[0]["id"]
                            res = self.__client.create_tweet(text=message, in_reply_to_tweet_id=id)
                        else:
                            media = self.__oauth_api.media_upload(image)
                            res = self.__client.create_tweet(text=message, media_ids=[media.media_id])
                    else:
                        media = self.__oauth_api.media_upload(image)
                        res = self.__client.create_tweet(text=message, media_ids=[media.media_id])
                elif message and not image:
                    res = self.__client.create_tweet(text=message)
                elif image and not message:
                    media = self.__oauth_api.media_upload(image)
                    res = self.__client.create_tweet(text=self.__only_img_mess, media_ids=[media.media_id])
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
                    if hash.startswith(self.__prefic):
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
            date_time = datetime.now(timezone.utc) - timedelta(hours=1.0)
            date_time_string = date_time.strftime("%Y-%m-%dT%H:%M:%SZ")
            tweets_data = self.__client.search_recent_tweets(
                query=f"(hiring OR opening) (@{self.__username}) -is:retweet -is:reply",
                max_results=100,
                start_time=date_time_string,
            )
            if tweets_data.data:
                for item in tweets_data.data:
                    item = dict(item)
                    tweet_id = item.get("id", 0)
                    tweet_info = self.tweet_info(tweet_id)
                    if tweet_info.get("token", ""):
                        data = {tweet_id: self.tweet_info(tweet_id)}
                        tweet_data.update(data)
        except Exception as mention_err:
            raise mention_err
        return tweet_data

    def re_tweet(self, tweet_id: int) -> bool:
        """
        Retweet the tweet about hiring or openings
        with a quote. You can change the default quote.
        argument:
            tweet_id: tweet id to be tweeted.
        """
        retweeted = False
        res = self.__client.create_tweet(text=self.__retweet_text, quote_tweet_id=tweet_id)
        return not retweeted
