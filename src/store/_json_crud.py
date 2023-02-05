import json
import logging
import os
import random
import string
from typing import Tuple


class JsonOperation:
    """
    Class for json operations are performed in the
    class. Functions implemented:
        file_name: for writing the users in the file.
        prefix: prefix for extracting token from json.
    """

    def __init__(self, file_name: str, prefix: str) -> None:
        self.__name = file_name
        self.__prefix = prefix
        self.st_error = False
        self.__logger = logging.getLogger("tweegramBot")
        self.__logger.info("store module is initialized.")

    def __read_record(self) -> dict:
        """
        reads the content of the file
        return:
            data: dictionary of all records
        """
        self.__logger.info("running %s", self.__read_record.__name__)
        with open(self.__name, "r") as read_file:
            data = json.load(read_file)
        return data

    def __write_record(self, data: dict) -> None:
        """
        writes the content to the json file.
        argument:
            data: content
        """
        self.__logger.info("running %s", self.__write_record.__name__)
        with open(self.__name, "w") as write_file:
            json.dump(data, write_file, indent=4)

    def create_token(self) -> str:
        """
        creates token, and makes sure the token
        is not a duplicate.
        return:
            token: token created
        """
        try:
            self.__logger.info("running %s", self.create_token.__name__)
            token = None
            if os.path.isfile(self.__name):
                while True:
                    self.__logger.info("checking if token already exists.")
                    token = "".join(random.choices(string.ascii_uppercase + string.digits, k=10))
                    data = self.__read_record()
                    token_list = [data[item].get("token", "") for item in data]
                    if token not in token_list:
                        break
            else:
                token = "".join(random.choices(string.ascii_uppercase + string.digits, k=10))
                self.__logger.info("token created")
        except Exception as token_err:
            self.__logger.error("Error in %s %s", self.create_token.__name__, token_err)
            self.st_error = True
            raise token_err
        return self.__prefix + token

    def add_user(self, user_name: str, token: str) -> bool:
        """
        Add user to the list with the token
        if not existing.
        argument:
            user_name: user to be added
            token: token for verification
        return:
            user_added: True if user is added
                        successfully
        """
        try:
            self.__logger.info("running %s", self.add_user.__name__)
            file_data = ""
            user_added = False
            data = {
                user_name: {
                    "user_name": user_name,
                    "token": token.replace(self.__prefix, ""),
                    "active": True,
                }
            }
            if os.path.isfile(self.__name):
                exists, active = self.check_user_exists(user_name)
                if exists and active:
                    user_added = False
                elif exists and not active:
                    file_data = self.__read_record()
                    file_data[user_name]["active"] = True
                elif not exists:
                    file_data = self.__read_record()
                    file_data.update(data)
            else:
                file_data = data
            if file_data:
                self.__write_record(file_data)
                user_added = True
                self.__logger.info("Adding new user.")
        except Exception as add_user_err:
            self.__logger.error("Error in %s %s", self.add_user.__name__, add_user_err)
            self.st_error = True
            raise add_user_err
        return user_added

    def check_user_exists(self, user_name: str) -> Tuple[bool, bool]:
        """
        Checks if a username exists in the json
        file.
        argument:
            username: against which the check should
                      run
        return:
            check: True if user exists
            active: True is user is active
        """
        try:
            self.__logger.info("running %s", self.check_user_exists.__name__)
            check, active = False, False
            if os.path.isfile(self.__name):
                data = self.__read_record()
                user_data = data.get(user_name, "")
                if user_data:
                    check = True
                    self.__logger.info("User exists in record.")
                    acitvity = user_data.get("active", "")
                    if acitvity:
                        active = True
                        self.__logger.info("User active in record.")
                    else:
                        self.__logger.warning("User not active in record.")
                        self.st_error = True
        except Exception as exist_err:
            self.__logger.error("Error in %s %s", self.check_user_exists.__name__, exist_err)
            self.st_error = True
            raise exist_err
        return check, active

    def remove_user(self, user_name: str) -> bool:
        """
        Removes the user from the json file.
        argument:
            username: against which the operation
            should be performed.
        return:
            user_removed: True if user is removed.
        """
        try:
            self.__logger.info("running %s", self.remove_user.__name__)
            user_removed = False
            exists, active = self.check_user_exists(user_name)
            if exists:
                if active:
                    data = self.__read_record()
                    data[user_name]["active"] = False
                    self.__write_record(data)
                    user_removed = True
                    self.__logger.info("Setting user active status to False.")
            else:
                self.__logger.warning("Username not found in record.")
                self.st_error = True
        except Exception as remove_err:
            self.__logger.error("Error in %s %s", self.remove_user.__name__, remove_err)
            self.st_error = True
            raise remove_err
        return user_removed

    def get_user_from(self):
        """
        Creating filter from the users in the
        json
        return:
            users_filter: filter string
        """
        try:
            self.__logger.info("running %s", self.get_user_from.__name__)
            users_filter = None
            keys = []
            if os.path.isfile(self.__name):
                data = self.__read_record()
                for key, value in data.items():
                    if value.get("active", False):
                        keys.append("from:" + key)
                    self.__logger.info("Creating filter for twitter.")
                users_filter = " OR ".join(keys)
            else:
                self.__logger.warning("No record file present.")
        except Exception as user_from_filter_err:
            self.__logger.error("Error in %s %s", self.get_user_from.__name__, user_from_filter_err)
            self.st_error = True
            raise user_from_filter_err
        return users_filter

    def verify(self, user_name: str, token: str) -> bool:
        """
        Verifies the tweet for retweet.
        argument:
            user_name: user
            token: token to verify for retweet
        """
        try:
            self.__logger.info("running %s", self.verify.__name__)
            verify = False
            exists, active = self.check_user_exists(user_name)
            if exists and active:
                data = self.__read_record()
                data = data.get(user_name, "")
                if data:
                    user_token = data.get("token", "")
                    user_user_name = data.get("user_name", "")
                    active = data.get("active", "")
                    if user_token == token and user_user_name == user_name and active:
                        self.__logger.info("User verified.")
                        verify = True
                    else:
                        self.__logger.warning("User not verified.")
                        self.st_error = True
                else:
                    self.__logger.warning("No such username in record.")
                    self.st_error = True
        except Exception as verify_err:
            self.__logger.error("Error in %s %s", self.verify.__name__, verify_err)
            self.st_error = True
            raise verify_err
        return verify
