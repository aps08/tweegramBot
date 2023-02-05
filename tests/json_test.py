import os
import re
import sys
import unittest

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from src import store


class Monolithic(unittest.TestCase):
    """
    Test cases for the json operations.
    Run the test functions one by one in order.
    """

    __name = "member_info.json"
    __prefix = "GTR_"
    __user = ("aps08__", "random_token")
    __newuser = ("hxlive", "random_token_two")
    __nouser = ("xccv", "random_token_two")

    def test_before_first_insert(self):
        """
        Test for first insert.
        """
        result = os.path.isfile(self.__name)
        self.assertEqual(result, False)

    def test_token_check(self):
        """
        Test for token format check.
        """
        fileobj = None
        fileobj = store(self.__name, self.__prefix)
        token = fileobj.create_token()
        token = token.split("_")[-1]
        if re.search("^[A-Z0-9]{10}$", token):
            result = True
        else:
            result = False
        self.assertEqual(result, True)

    def test_add_new_user(self):
        """
        Test case for new user
        """
        fileobj = None
        fileobj = store(self.__name, self.__prefix)
        added = fileobj.add_user(self.__user[0], self.__user[1])
        self.assertEqual(added, True)

    def test_after_first_insert(self):
        """
        Test for first insert.
        """
        result = os.path.isfile(self.__name)
        self.assertEqual(result, True)

    def test_user_exists(self):
        """
        Test case of user exists and active
        """
        fileobj = None
        fileobj = store(self.__name, self.__prefix)
        added = fileobj.add_user(self.__user[0], self.__user[1])
        self.assertEqual(added, False)

    def test_add_another_user(self):
        """
        Add second user.
        """
        fileobj = None
        fileobj = store(self.__name, self.__prefix)
        added = fileobj.add_user(self.__newuser[0], self.__newuser[1])
        self.assertEqual(added, True)

    def test_remove_user(self):
        """
        Test case of changing activity of user
        """
        fileobj = None
        fileobj = store(self.__name, self.__prefix)
        removed = fileobj.remove_user(self.__user[0])
        self.assertEqual(removed, True)

    def test_user_not_found(self):
        """
        Test case when user doesn't in record
        """
        fileobj = None
        fileobj = store(self.__name, self.__prefix)
        exists, active = fileobj.check_user_exists("fireOx")
        self.assertEqual(exists, False)
        self.assertEqual(active, False)

    def test_unactive_user(self):
        """
        Test case to check unactive user
        """
        fileobj = None
        fileobj = store(self.__name, self.__prefix)
        exists, active = fileobj.check_user_exists(self.__user[0])
        self.assertEqual(exists, True)
        self.assertEqual(active, False)

    def test_verify_no_user(self):
        """
        Verify for user which doesn't exists
        """
        fileobj = None
        fileobj = store(self.__name, self.__prefix)
        verified = fileobj.verify(self.__nouser[0], self.__nouser[1])
        self.assertEqual(verified, False)

    def test_remove_user_no_user(self):
        """
        Test case for removing user which doesn't exists
        """
        fileobj = None
        fileobj = store(self.__name, self.__prefix)
        removed = fileobj.remove_user("xccwewd")
        self.assertEqual(removed, False)

    def test_remove_already_removed_user(self):
        """
        Test case of changing activity of user
        """
        fileobj = None
        fileobj = store(self.__name, self.__prefix)
        removed = fileobj.remove_user(self.__name[0])
        self.assertEqual(removed, False)

    def test_verify_user(self):
        """
        Verify for user, id and token
        """
        fileobj = None
        fileobj = store(self.__name, self.__prefix)
        verified = fileobj.verify(self.__newuser[0], self.__newuser[1])
        self.assertEqual(verified, True)
