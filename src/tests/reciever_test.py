import os
import sys
import unittest

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from receiver import receiver


class Monolithic(unittest.TestCase):
    """
    Test cases for the twitter operations.
    Run the test functions one by one in order.
    """

    __username = "tech_referrals"
    __username_2 = "code_writing"
    __user_id = 1617568257833304064
    __tweet_id = 1621823395666210816

    def test_remove_media(self):
        """
        Test for removing media file
        when it doesn't exists.
        """
        receiverobj = None
        receiverobj = receiver(username=self.__username)
        removed = receiverobj.remove_media()
        self.assertEqual(removed, False)

    def test_remove_media2(self):
        """
        Test for removing media file
        when it exists.
        """
        receiverobj = None
        receiverobj = receiver(username=self.__username)
        removed = receiverobj.remove_media()
        self.assertEqual(removed, True)

    def test_get_id(self):
        """
        Test for getting id against username
        """
        receiverobj = None
        receiverobj = receiver(username=self.__username)
        id = receiverobj.get_user_id(user_name=self.__username_2)
        self.assertEqual(id, self.__user_id)

    def test_get_username(self):
        """
        Test for getting username against id
        """
        receiverobj = None
        receiverobj = receiver(username=self.__username)
        user_name = receiverobj.get_user_id(author_id=self.__user_id)
        self.assertEqual(user_name, self.__username_2)

    def test_retweet(self):
        """
        Test case to retweet
        """
        receiverobj = None
        receiverobj = receiver(username=self.__username)
        retweeted = receiverobj.re_tweet(self.__tweet_id)
        self.assertEqual(retweeted, True)

    def test_mentions(self):
        """
        Test case for checking mentioned tweets
        """
        receiverobj = None
        receiverobj = receiver(username=self.__username)
        data = receiverobj.get_mentioned_tweets()
        data = data[self.__tweet_id]
        self.assertEqual(data["author_id"], self.__user_id)
        self.assertEqual(data["username"], self.__username_2)

    def test_tweet_info(self):
        """
        Test case for checking tweet info
        like authord id, name and token (if any)
        """
        receiverobj = None
        receiverobj = receiver(username=self.__username)
        data = receiverobj.tweet_info(self.__tweet_id)
        self.assertEqual(data["author_id"], self.__user_id)
        self.assertEqual(data["username"], self.__username_2)
        self.assertEqual(data["token"], None)
