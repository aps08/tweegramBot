"""
This file is reponsible for performing insert,
delete and remove in json file. Also responsible
for storing stats.
"""
import json
import os
import random
import string
from typing import Tuple


class JsonOperation:
    """
    Class for json operations are performed in the
    class. Functions implemented:
        read_record: for reading the content of the json.
        read_record: for writing the given content in the file.
        create_token: creates token of 10 chars, and contains
                    upper case alphabets and digits.
        add_user: adds user to the json, if it's first time
                insert, then creates the json file.
        remove_user: removes or change the activity of a user
                to false.
        check_user_exists: checks if user already exists or not.
                        Also checks if that user is active.
        verify: verifies if the user is present and the token used
                is correct or not.

    """

    def __init__(self, file_name: str = "member_info.json") -> None:
        self.__name = file_name

    def __read_record(self) -> dict:
        """
        reads the content of the file
        return:
            data: dictionary of all records
        """
        with open(self.__name, "r") as read_file:
            data = json.load(read_file)
        return data

    def __write_record(self, data: dict) -> None:
        """
        writes the content to the json file.
        argument:
            data: content
        """
        with open(self.__name, "w") as write_file:
            json.dump(data, write_file, indent=4)

    def create_token(self) -> str:
        """
        creates token,and makes sure the token
        is not a duplicate
        return:
            token: token created
        """
        try:
            token = None
            prefix = "GTR_"
            if os.path.isfile(self.__name):
                while True:
                    token = "".join(random.choices(string.ascii_uppercase + string.digits, k=10))
                    data = self.__read_record()
                    token_list = [data[item].get("token", "") for item in data]
                    if token not in token_list:
                        break
            else:
                token = "".join(random.choices(string.ascii_uppercase + string.digits, k=10))
        except Exception as token_err:
            raise token_err
        return prefix + token

    def add_user(self, user_name: str, token: str, id: int) -> bool:
        """
        Add user to the list with the token
        if not existing.
        argument:
            user_name: user to be added
            token: token for verification
            id: twitter id of the username
        return:
            user_added: True if user is added
                        successfully
        """
        try:
            file_data = ""
            user_added = False
            data = {
                user_name: {
                    "user_name": user_name,
                    "id": id,
                    "token": token,
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
        except Exception as add_user_err:
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
            check, active = False, False
            if os.path.isfile(self.__name):
                data = self.__read_record()
                user_data = data.get(user_name, "")
                if user_data:
                    check = True
                    acitvity = user_data.get("active", "")
                    if acitvity:
                        active = True
        except Exception as exist_err:
            raise exist_err
        return check, active

    def remove_user(self, user_name: str) -> bool:
        """
        Removes the user from the json file.
        argument:
            username: against which the operation
            should be performed
        return:
            user_removed: True if user is removed.
        """
        try:
            user_removed = False
            exists, active = self.check_user_exists(user_name)
            if exists:
                if active:
                    data = self.__read_record()
                    data[user_name]["active"] = False
                    self.__write_record(data)
                    user_removed = True
        except Exception as remove_err:
            raise remove_err
        return user_removed

    def verify(self, user_name: str, token: str, id: int) -> bool:
        """
        Verifies the tweet for retweet.
        argument:
            id: tweeter id of the user.
            user_name: user
            token: token to verify for retweet
        """
        try:
            verify = False
            exists, active = self.check_user_exists(user_name)
            if exists and active:
                data = self.__read_record()[user_name]
                user_id = data.get("id", "")
                user_token = data.get("token", "")
                user_user_name = data.get("user_name", "")
                if user_id == id and user_token == token and user_user_name == user_name:
                    verify = True
        except Exception as verify_err:
            raise verify_err
        return verify
