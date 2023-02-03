import os
import sys
import unittest

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from sender import sender


class Monolithic(unittest.TestCase):
    """
    Test cases for the telegram operations.
    Run the test functions one by one in order.
    """

    __messages = [
        {"message": "@notice Notice all"},
        {"message": "I'm working on tweegramBot"},
        {"message": "@remove aps08__"},
    ]

    def test_empty_list(self):
        """
        Test case for passing empty
        list in command check
        """
        senderobj = None
        senderobj = sender()
        data = senderobj.command_check([])
        self.assertEqual(data, ([], []))

    def test_send_message(self):
        """
        Test case for sending message
        to yourself on telegram
        """
        senderobj = None
        senderobj = sender()
        sent = senderobj.send_message("me")
        self.assertEqual(sent, True)

    def test_when_cc_false(self):
        """
        Test case when command check is false
        """
        senderobj = None
        senderobj = sender()
        comm, mess = senderobj.get_messages(text=True, image=True)
        self.assertEqual(comm, [])
        self.assertEqual(len(mess) > 1, True)

    def test_when_tc_true(self):
        """
        Test case when command check is True
        """
        senderobj = None
        senderobj = sender(command_check=True)
        comm, mess = senderobj.get_messages(text=True, image=True)
        self.assertEqual(len(comm) > 1, True)
        self.assertEqual(len(mess) > 1, True)

    def test_command_check(self):
        """
        Test case for checking if the commands
        are getting seperated from normal messages
        """
        senderobj = None
        senderobj = sender(command_check=True)
        comm, mess = senderobj.command_check(self.__messages)
        self.assertEqual(len(comm), 1)
        self.assertEqual(len(mess), 1)
