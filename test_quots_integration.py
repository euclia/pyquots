import unittest
from pyquots import IPyquots, Pyquots, errors
from pyquots.pyquots_named_tuples import *


class TestPyquots(unittest.TestCase):

    def setUp(self):
        self.pyquots = Pyquots('127.0.0.1:8002', 'Pyquots', 'x2P4IIFbldc&kVOMZn')

    def tearDown(self):
        self.pyquots.close()

    def test_create_user(self):
        print("Testing creating user")
        qu = QuotsUser(id="quotsuserid", email='quotsuseremail', username='pyquotsusername')
        try:
            quc = self.pyquots.create_user(qu)
            self.assertEqual(quc.id, "quotsuserid")
        except errors.QuotsError as quer:
            self.assertEqual(quer.status, 409)

    def test_get_user(self):
        try:
            print("Testing getting user")
            qug = self.pyquots.get_user(userid="quotsuserid")
            self.assertEqual(qug.id, "quotsuserid")
        except errors.UserNotFound as unf:
            self.assertEqual(unf.status, 404)

    def test_can_user_proceed(self):
        try:
            print("Testing can user proceed")
            cp = self.pyquots.can_user_proceed("quotsuserid", "TASK", "1")
            self.assertEqual(cp.proceed, True)
        except errors.UserNotFound as unf:
            self.assertEqual(unf.status, 500)

    def test_could_not_find_usage(self):
        try:
            print("Testing can user proceed / not found usage")
            cp = self.pyquots.can_user_proceed("quotsuserid", "Task", "1")
            self.assertEqual(cp.proceed, True)
        except errors.CannotProceedError as unf:
            self.assertEqual(unf.message, "Cound not find usage")

    def test_update_user_credits(self):
        try:
            print("Testing update user's credits")
            ud = QuotsUser(id="quotsuserid", email='quotsuseremail', username='pyquotsusername', credits=40.0)
            updu = self.pyquots.update_user_credits(ud)
            self.assertEqual(updu.credits, 40.0)
        except errors.UserNotFound as unf:
            self.assertEqual(unf.status, 404)

    def delete_user(self):
        try:
            print("dDeleting user")
            dele = self.pyquots.delete_user("quotsuserid")
            self.assertEqual(dele, True)
        except errors.QuotsError as qe:
            self.assertEqual(qe.status, 500)

    if __name__ == '__main__':
        unittest.main()