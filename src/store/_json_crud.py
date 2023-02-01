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
    All json operations are performed in the
    class.
    """

    def __init__(self) -> None:
        self.__name = "member_info.json"
        # decrypt things here.

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
                    with open(self.__name, "r") as read_file:
                        data = json.load(read_file)
                        token_list = [item["token"] for item in data]
                        if token not in token_list:
                            break
            else:
                token = "".join(random.choices(string.ascii_uppercase + string.digits, k=10))
        except Exception as token_err:
            raise token_err
        return prefix + token

    def add_user(self, user_name: str, id: str) -> bool:
        """
        Add user to the list with the token
        if not existing.
        argument:
            user_name: user to be added
            id: twitter id of the username
        return:
            user_added: True if user is added
                        successfully
        """
        try:
            user_added = False
            data = {
                user_name: {
                    "user_name": user_name,
                    "id": id,
                    "token": self.create_token(),
                    "active": True,
                }
            }
            if os.path.isfile(self.__name):
                exists, active = self.check_user_exists(user_name)
                if exists and active:
                    raise ValueError("User already exists.")
                elif exists and not active:
                    with open(self.__name, "r") as read_file:
                        file_data = json.load(read_file)
                        file_data[user_name]["active"] = True
                elif not exists:
                    with open(self.__name, "r") as read_file:
                        file_data = json.load(read_file)
                        file_data.update(data)
            else:
                file_data = data
            with open(self.__name, "w") as write_file:
                json.dump(file_data, write_file, indent=4)
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
            with open(self.__name, "r") as read_file:
                data = json.load(read_file)
                if user_name in data:
                    if data[user_name]["active"]:
                        check, active = True, True
                    else:
                        check, active = True, False
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
            if os.path.isfile(self.__name):
                exists, active = self.check_user_exists(user_name)
                if exists:
                    if active:
                        with open(self.__name, "r+") as rw_file:
                            data = json.load(rw_file)
                            data[user_name]["active"] = False
                            rw_file.seek(0)
                            json.dump(data, rw_file, indent=4)
                            user_removed = True
                    else:
                        raise ValueError("User already deleted.")
                else:
                    raise ValueError("User doesn't exists in the record.")
            else:
                raise ValueError(
                    f"{self.__name} doesn't exists. Can't remove user from a file which doesn't exists"
                )
        except Exception as remove_err:
            raise remove_err
        return user_removed
