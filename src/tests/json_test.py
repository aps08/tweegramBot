import os
import re
import sys
import time
import unittest

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
unittest.TestLoader.sortTestMethodsUsing = None
from store import file


class Monolithic(unittest.TestCase):
    """
    Test cases for the json operations.
    Run the test functions one by one in order.
    """

    __name = "member_info.json"

    def test_1_before_first_insert(self):
        """
        Test for first insert.
        """
        result = os.path.isfile(self.__name)
        self.assertEqual(result, False)

    def test_2_token_check(self):
        """
        Test for token format check.
        """
        fileobj = None
        fileobj = file()
        token = fileobj.create_token()
        token = token.split("_")[-1]
        if re.search("^[A-Z0-9]{10}$", token):
            result = True
        else:
            result = False
        self.assertEqual(result, True)

    def test_3_add_new_user(self):
        """
        Test case for new user
        """
        fileobj = None
        fileobj = file()
        added = fileobj.add_user("aps08__", "random_token", 13243534)
        self.assertEqual(added, True)

    def test_4_after_first_insert(self):
        """
        Test for first insert.
        """
        result = os.path.isfile(self.__name)
        self.assertEqual(result, True)

    def test_5_user_exists(self):
        """
        Test case of user exists and active
        """
        fileobj = None
        fileobj = file()
        added = fileobj.add_user("aps08__", "random_token", 13243534)
        self.assertEqual(added, False)

    def test_6_add_another_user(self):
        """
        Add second user.
        """
        fileobj = None
        fileobj = file()
        added = fileobj.add_user("hxlive", "random_token_two", 7544324)
        self.assertEqual(added, True)

    def test_7_remove_user(self):
        """
        Test case of changing activity of user
        """
        fileobj = None
        fileobj = file()
        removed = fileobj.remove_user("aps08__")
        self.assertEqual(removed, True)

    def test_8_user_not_found(self):
        """
        Test case when user doesn't in record
        """
        fileobj = None
        fileobj = file()
        exists, active = fileobj.check_user_exists("fireOx")
        self.assertEqual(exists, False)
        self.assertEqual(active, False)

    def test_9_unactive_user(self):
        """
        Test case to check unactive user
        """
        fileobj = None
        fileobj = file()
        exists, active = fileobj.check_user_exists("aps08__")
        self.assertEqual(exists, True)
        self.assertEqual(active, False)

    def test_10_verify_no_user(self):
        """
        Verify for user which doesn't exists
        """
        fileobj = None
        fileobj = file()
        verified = fileobj.verify("xccv", "random_token_two", 7544324)
        self.assertEqual(verified, False)

    def test_11_remove_user_no_user(self):
        """
        Test case for removing user which doesn't exists
        """
        fileobj = None
        fileobj = file()
        removed = fileobj.remove_user("xccwewd")
        self.assertEqual(removed, False)

    def test_12_remove_already_removed_user(self):
        """
        Test case of changing activity of user
        """
        fileobj = None
        fileobj = file()
        removed = fileobj.remove_user("aps08__")
        self.assertEqual(removed, False)

    def test_13_verify_user(self):
        """
        Verify for user, id and token
        """
        fileobj = None
        fileobj = file()
        verified = fileobj.verify("hxlive", "random_token_two", 7544324)
        self.assertEqual(verified, True)


if __name__ == "__main__":
    unittest.main()
