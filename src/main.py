from receiver import receiver
from sender import sender
from store import store


class TweegramBot(receiver, sender, store):
    def __init__(
        self,
        username: str,
        first_comment: bool = False,
        command_check: bool = False,
        file_name: str = "member_info.json",
        prefix: str = "GTR_",
        retweet_text: str = "Retweeting for better reach. \U0001F603",
        add_message: str = """Thank you for joining us @{}.You have been added to our list with #{}.Tag us with this token as hashtag.""",
        remove_message: str = "{} tweeter user has been removed.",
        only_img_mess: str = "Opening \U0001F603",
    ) -> None:
        receiver.__init__(
            self,
            username=username,
            first_comment=first_comment,
            prefix=prefix,
            retweet_text=retweet_text,
            only_img_mess=only_img_mess,
        )
        sender.__init__(self, command_check=command_check)
        store.__init__(self, file_name=file_name, prefix=prefix)
        self.__add_message = add_message
        self.__remove_message = remove_message

    def command_execution(self, commands: list) -> None:
        """
        Executes command given in the list
        argument:
            commands: list of commands
        """
        try:
            for command in commands:
                if command.startswith("@add"):
                    user = command.split(" ")[-1]
                    id = self.get_user_id(user_name=user)
                    if id:
                        token = self.create_token()
                        user_added = self.add_user(user, token, id)
                        if user_added:
                            notification_tweet = self.__add_message.format(user, token)
                            self.convert_to_tweet([{"message": notification_tweet, "image": None}])
                if command.startswith("@remove"):
                    user = command.split(" ")[-1]
                    if self.remove_user(user):
                        telegram_notification = self.__remove_message.format(user)
                        self.send_message(text=telegram_notification)
        except Exception as comm_exe_err:
            raise comm_exe_err

    def retrieving(self) -> None:
        commands, messages = self.get_messages()
        if self.check and commands:
            self.command_execution(commands)
        if messages:
            self.convert_to_tweet(messages)

    def increase_reach(self) -> None:
        items = self.get_mentioned_tweets()
        for tweet_id, author_data in items.items():
            author_id = author_data.get("author_id", "")
            token = author_data.get("token", "")
            username = author_data.get("username", "")
            if author_id and token and username:
                verified = self.verify(username, token, author_id)
                if verified:
                    self.re_tweet(tweet_id)

    def start(self) -> None:
        self.retrieving()
        self.increase_reach()
        self.remove_media()


TweegramBot = TweegramBot(username="tech_referrals", command_check=True)
TweegramBot.start()
