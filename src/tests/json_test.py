import os
import re
import sys
import unittest

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from store import file


class TestCase(unittest.TestCase):
    """
    Test cases for the json operations.
    """

    def test_token_check(self):
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

    def test_file_created(self):
        """
        Test for first insert.
        """
        pass

    def test_add_new_user(self):
        """
        Test case for new user
        """
        pass

    def test_user_exists(self):
        """
        Test case of user exists and active
        """
        pass

    def test_remove_user(self):
        """
        Test case of changing activity of user
        """
        pass

    def test_unactive_user(self):
        """
        Test case to check unactive user
        """
        pass


if __name__ == "__main__":
    unittest.main()
