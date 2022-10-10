"""
Module is responsible for converting 
telegram messages to twitter tweets.
"""

import os
import shutil
from datetime import datetime, timedelta, timezone

import tweepy
from telethon.sync import TelegramClient

import config


class TelegramToTweet:
    """
    This class is responsible for reading text
    from telegram group and converting it to twitter
    tweets.
    """

    def __get_messages(self) -> list:
        """
        Downloads media and texts from telegram group
        for past 1 day.
        """
        items = []
        date_time = datetime.now(timezone.utc) - timedelta(days=2.0)
        try:
            with TelegramClient("aps08", config.TEL_API_ID, config.TEL_API_HASH) as client:
                media_count = 0
                for message in client.iter_messages(config.TEL_GROUP):
                    export_path = f"src\\media\\{media_count}"
                    if message.date > date_time:
                        temp_dict = {}
                        if message.photo:
                            path = client.download_media(message, export_path)
                            temp_dict["media_path"] = path
                            temp_dict["message"] = message.text
                        else:
                            temp_dict["message"] = message.text
                        items.append(temp_dict)
                        media_count += 1
        except Exception as down_err:
            raise down_err
        return items

    def __send_tweet(self, items: dict) -> None:
        """
        Iterate dictionary items and converts
        them into tweet.
        """
        try:
            client = tweepy.Client(
                consumer_key=config.TWT_API_KEY,
                consumer_secret=config.TWT_API_SECRET,
                access_token=config.TWT_ACCESS_TOKEN,
                access_token_secret=config.TWT_ACCESS_TOKEN_SECRET,
            )
            auth = tweepy.OAuthHandler(
                consumer_key=config.TWT_API_KEY,
                consumer_secret=config.TWT_API_SECRET,
                access_token=config.TWT_ACCESS_TOKEN,
                access_token_secret=config.TWT_ACCESS_TOKEN_SECRET,
            )
            twitter_api = tweepy.API(auth)
            for item in items:
                message = item.get("message", "")
                media_path = item.get("media_path", "")
                if message and media_path:
                    media = twitter_api.media_upload(media_path)
                    res = client.create_tweet(text=message, media_ids=[media.media_id])
                elif message and not media_path:
                    res = client.create_tweet(text=message)
                elif not message and media_path:
                    media = twitter_api.media_upload(media_path)
                    res = client.create_tweet(text="Opportunity", media_ids=[media.media_id])
                else:
                    print("something is not right.")
                    break
        except Exception as send_err:
            raise send_err

    def __delete_media_dir(self) -> None:
        """
        Deletes media directory after use.
        """
        try:
            current_dir = os.getcwd()
            path = os.path.join(current_dir, "src\\media")
            shutil.rmtree(path)
            os.remove("aps08.session")
        except Exception as del_err:
            raise del_err

    def start(self) -> None:
        """
        Trigger the class from here.
        """
        try:
            items = self.__get_messages()
            self.__send_tweet(items=items)
            self.__delete_media_dir()
        except Exception as start_err:
            raise start_err


if __name__ == "__main__":
    TelegramToTweet = TelegramToTweet()
    TelegramToTweet.start()
