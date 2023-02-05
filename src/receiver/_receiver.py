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

    def remove_media(self) -> bool:
        """
        Fully remove the media folder.
        return:
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
        argument:
            items:  list of dictionaries, where each
            dictionary contain message and image key.
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

    def get_user_id(self, user_name: str) -> bool:
        """
        Checks if user_name exists in twitter or not.
        argument:
            user_name: username againt which check is needed.
        return:
            result: id or username as per input
        """
        try:
            result = False
            user_data = self.__client.get_user(username=user_name)
            if user_data.data:
                result = True
        except Exception as user_err:
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
            tweet_data = list()
            date_time = datetime.now(timezone.utc) - timedelta(hours=1.0)
            date_time_string = date_time.strftime("%Y-%m-%dT%H:%M:%SZ")
            print(f"(hiring OR opening) ({users}) (@{self.__username}) -is:retweet -is:reply")
            tweets_data = self.__client.search_recent_tweets(
                query=f"(hiring OR opening) ({users}) (@{self.__username}) -is:retweet -is:reply",
                expansions=["entities.mentions.username", "author_id"],
                max_results=100,
                start_time=date_time_string,
            )
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
            raise mention_err
        return tweet_data

    def re_tweet(self, tweet_id: int) -> bool:
        """
        Retweet the tweet about hiring or openings
        with a quote. You can change the default quote.
        argument:
            tweet_id: tweet id to be tweeted.
        """
        res = self.__client.create_tweet(text=self.__retweet_text, quote_tweet_id=tweet_id)
