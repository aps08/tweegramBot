import logging
import os
import re
import shutil
from datetime import datetime, timedelta, timezone

import tweepy
from tweepy.api import API
from tweepy.client import Client
from validator_collection import checkers


class Creator:
    """
    Creates required objects for twitter API calls.
    """

    def get_client(self) -> Client:
        """
        Public function to create and return Client object.
        return:
            client: twitter client object.
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
        Public function to create and return OAuth object.
        return:
            auth: twitter OAuth object.
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
    first_comment : default value False, change it to True.
                    It is mandatory to pass only link as caption
                    of an image if True. Otherwise the link
                    will not be tweeted in first comment.
    username : twitter username of the bot
    prefix : prefix to identify token from the hashtags
    retweet_text : Quote for retweet. Can't retweet with without
                    quote.
    only_img_mess : Text when the tweet is only image.
    """

    def __init__(self, username: str, first_comment: bool, prefix: str, retweet_text: str, only_img_mess: str):
        """constructor"""
        Creator.__init__(self)
        self.__client = self.get_client()
        self.__oauth_api = self.get_oauth()
        self.__first_comment = first_comment
        self.__username = username
        self.__retweet_text = retweet_text
        self.__prefix = prefix
        self.__only_img_mess = only_img_mess
        self.r_error = False
        self.__logger = logging.getLogger("tweegramBot")
        self.__logger.info("receiver module is initialized.")

    def remove_media(self) -> bool:
        """
        Fully remove the media folder.
        return:
            removed: True if folder is removed.
        """
        try:
            self.__logger.info("running %s", self.remove_media.__name__)
            removed = False
            current_dir = os.getcwd()
            path = os.path.join(current_dir, "media")
            if os.path.exists(path):
                shutil.rmtree(path)
                self.__logger.info("media folder removed.")
                removed = True
        except Exception as del_err:
            self.__logger.error("Error in %s %s", self.remove_media.__name__, del_err)
            self.r_error = True
            raise del_err
        return removed

    def convert_to_tweet(self, items: list) -> None:
        """
        Iterate list items and converts
        them into tweet.
        argument:
            items:  list of dictionaries, where each
            dictionary contain message and image key.
        """
        try:
            self.__logger.info("running %s", self.convert_to_tweet.__name__)
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
                            self.__logger.info("Tweeting with link in first comment.")
                        else:
                            media = self.__oauth_api.media_upload(image)
                            res = self.__client.create_tweet(text=message, media_ids=[media.media_id])
                            self.__logger.info("Tweeting with link in the tweet. Not everthing in the text is a link")
                    else:
                        media = self.__oauth_api.media_upload(image)
                        res = self.__client.create_tweet(text=message, media_ids=[media.media_id])
                        self.__logger.info("Tweeting with image and text")
                elif message and not image:
                    res = self.__client.create_tweet(text=message)
                    self.__logger.info("Tweeting with only text")
                elif image and not message:
                    media = self.__oauth_api.media_upload(image)
                    res = self.__client.create_tweet(text=self.__only_img_mess, media_ids=[media.media_id])
                    self.__logger.info("Tweeting with only image, with custom caption text.")
        except Exception as send_tweet_err:
            self.__logger.error("Error in %s %s", self.convert_to_tweet.__name__, send_tweet_err)
            self.r_error = True
            raise send_tweet_err

    def get_user_id(self, user_name: str) -> bool:
        """
        Checks if user_name exists in twitter or not.
        argument:
            user_name: username againt which check is needed.
        return:
            result: id or username as per input
        """
        try:
            self.__logger.info("running %s", self.get_user_id.__name__)
            result = False
            user_data = self.__client.get_user(username=user_name)
            if user_data.data:
                result = True
                self.__logger.info("user found on twitter.")
        except Exception as user_err:
            self.__logger.error("Error in %s %s", self.get_user_id.__name__, user_err)
            self.r_error = True
            raise user_err
        return result

    def get_mentioned_tweets(self, users: str) -> list:
        """
        Gets tweet where the bot is mentioned.
        argument:
            users: filter for from keyword in search
        return:
            tweet_data: list of dictionary with tweet_id and token
        """
        try:
            self.__logger.info("running %s", self.get_mentioned_tweets.__name__)
            tweet_data = list()
            date_time = datetime.now(timezone.utc) - timedelta(hours=1.0)
            date_time_string = date_time.strftime("%Y-%m-%dT%H:%M:%SZ")
            tweets_data = self.__client.search_recent_tweets(
                query=f"(hiring OR opening) ({users}) (@{self.__username}) -is:retweet -is:reply",
                expansions=["entities.mentions.username", "author_id"],
                max_results=100,
                start_time=date_time_string,
            )
            self.__logger.info("Getting mentioned tweets in last one hour.")
            if tweets_data.data and tweets_data.includes:
                for tweet, user in zip(tweets_data.data, tweets_data.includes["users"]):
                    tweet = dict(tweet)
                    user = dict(user)
                    tweet_id = tweet.get("id", 0)
                    text = tweet.get("text", "")
                    username = user.get("username", "")
                    if tweet_id and text and username:
                        hash_list = re.findall("#(\w+)", text)
                        hash_token = [hash_token for hash_token in hash_list if hash_token.startswith(self.__prefix)]
                        if hash_token:
                            hash_token = hash_token[0].split("_")[-1]
                            tweet_data.append({"tweet_id": tweet_id, "token": hash_token, "username": username})
        except Exception as mention_err:
            self.__logger.error("Error in %s %s", self.get_mentioned_tweets.__name__, mention_err)
            self.r_error = True
            raise mention_err
        return tweet_data

    def re_tweet(self, tweet_id: int) -> bool:
        """
        Retweet the tweet about hiring or openings
        with a quote. You can change the default quote.
        argument:
            tweet_id: tweet id to be tweeted.
        """
        try:
            self.__logger.info("running %s", self.re_tweet.__name__)
            res = self.__client.create_tweet(text=self.__retweet_text, quote_tweet_id=tweet_id)
            self.__logger.info("retweeted.")
        except Exception as retweet_err:
            self.__logger.error("Error in %s %s", self.re_tweet.__name__, retweet_err)
            self.r_error = True
            raise retweet_err
