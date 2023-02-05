import io
import logging
import os

from dotenv import load_dotenv

from receiver import receiver
from sender import sender
from store import store

load_dotenv()
io_string = io.StringIO()
logger = logging.getLogger("tweegramBot")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(io_string)
handler.setFormatter(logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(message)s"))
if logger.hasHandlers():
    logger.handlers.clear()
logger.addHandler(handler)


class Default:
    """
    All default configuration.
    """

    USERNAME = os.environ.get("USERNAME")
    FIRST_COMMENT: bool = False
    COMMAND_CHECK: bool = True
    FILE_NAME: str = "member_info.json"
    PREFIX: str = "GTR_"
    RETWEET_TEXT: str = "Retweeting for better reach. \U0001F603"
    ADD_MESSAGE: str = """Thank you for joining us @{}.You have been added to our list with #{}."""
    REMOVE_MESSAGE: str = "{} tweeter user has been removed."
    ONLY_IMG_MESSAGE: str = "Opening \U0001F603"
    RETWEET_MENTIONED: bool = True
    SEND_LOG_ON_ERR: bool = True
    logger.info("Configuration variables set.")


class TweegramBot(receiver, sender, store, Default):
    """
    class is responsible for running the mail flow.
    Inherited classes:
        receiver: where twitter operations are performed
        sender: where telegram operations are performed
        store: where json operations are performed
        Config: where all default configuration is set
    """

    def __init__(self) -> None:
        """constructur"""
        Default.__init__(self)
        receiver.__init__(
            self,
            username=self.USERNAME,
            first_comment=self.FIRST_COMMENT,
            prefix=self.PREFIX,
            retweet_text=self.RETWEET_TEXT,
            only_img_mess=self.ONLY_IMG_MESSAGE,
        )
        sender.__init__(self, command_check=self.COMMAND_CHECK)
        store.__init__(self, file_name=self.FILE_NAME, prefix=self.PREFIX)
        self.__add_message = self.ADD_MESSAGE
        self.__remove_message = self.REMOVE_MESSAGE
        self.__re_tweet_mentioned = self.RETWEET_MENTIONED
        logger.info("Main class initialized")

    def command_execution(self, commands: list) -> None:
        """
        Executes command given in the list
        argument:
            commands: list of commands
        """
        try:
            logger.info("running %s", self.command_check.__name__)
            for command in commands:
                if command.startswith("@add"):
                    user = command.split(" ")[-1]
                    if self.get_user_id(user_name=user):
                        token = self.create_token()
                        user_added = self.add_user(user, token)
                        if user_added:
                            logger.info("Added user, sending notification on twitter")
                            notification_tweet = self.__add_message.format(user, token)
                            self.convert_to_tweet([{"message": notification_tweet, "image": None}])
                if command.startswith("@remove"):
                    user = command.split(" ")[-1]
                    if self.remove_user(user):
                        telegram_notification = self.__remove_message.format(user)
                        logger.info("Removed user, sending notification on telegram")
                        self.send_message(text=telegram_notification)
        except Exception as comm_exe_err:
            logger.error("Error in %s %s", self.command_check.__name__, comm_exe_err)
            raise comm_exe_err

    def increase_reach(self) -> None:
        """
        Fectches mentioned tweets in last one hour,
        and retweet with quote if token and user is in
        the list.
        """
        try:
            logger.info("running %s", self.increase_reach.__name__)
            if self.__re_tweet_mentioned:
                filter_by_users = self.get_user_from()
                items = self.get_mentioned_tweets(filter_by_users)
                for author_data in items:
                    token = author_data.get("token", "")
                    tweet_id = author_data.get("tweet_id", "")
                    username = author_data.get("username", "")
                    if token and tweet_id and username:
                        verified = self.verify(username, token)
                        if verified:
                            logger.info("retweeting verified tweet.")
                            self.re_tweet(tweet_id)
                        else:
                            logger.warning("verification failed, can't retweet.")
                    else:
                        logger.warning("one of the value in token,tweet_id,username is not foound.")
        except Exception as reach_err:
            logger.error("Error in %s %s", self.increase_reach.__name__, reach_err)
            raise reach_err

    def start(self) -> None:
        """
        Function is the entry point of the flow.
        """
        try:
            logger.info("running %s", self.start.__name__)
            commands, messages = self.get_messages()
            if self.check and commands:
                self.command_execution(commands)
            if messages:
                self.convert_to_tweet(messages)
            self.increase_reach()
            self.remove_media()
        except Exception as start_err:
            logger.error("Error in %s %s", self.start.__name__, start_err)
        finally:
            if self.SEND_LOG_ON_ERR and (self.st_error or self.s_error or self.r_error):
                self.send_message(text=io_string.getvalue())


if __name__ == "__main__":
    TweegramBot = TweegramBot()
    TweegramBot.start()
