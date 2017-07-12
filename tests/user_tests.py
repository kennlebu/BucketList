import unittest
from datetime import datetime
from ..app.user import User
from ..app.bucket_list import BucketList

class UserTests(unittest.TestCase):
    """ Tests for the user class """

    def test_user(self):
        """ Test creation of the user class """

        user = User('kennlebu', 'password', 'Kenneth', 'Lebu', 24)

        assert user
        self.assertEqual(user.username, 'kennlebu', msg='Username should be kennlebu')
        self.assertEqual(user.age, 24, msg='Age should be 24')

    def test_add_bucketlist(self):
        """ Test whether a user can add a bucketlist """

        user = User('kennlebu', 'password', 'Kenneth', 'Lebu', 24)
        user.create_bucketlist("Go to China", datetime.now().strftime('%Y-%m-%d'))
        user.create_bucketlist("Buy an island", datetime.now().strftime('%Y-%m-%d'))

        # Check whether the bucket lists have been created
        self.assertEqual(2, len(user.bucketlists), msg='User should have 2 bucketlists')

        # Check whether the created objects are of BucketList type
        for item in user.bucketlists:
            assert isinstance(item, BucketList)

    def test_remove_bucketlist(self):
        """ Test whether a user can remove a bucketlist """

        user = User('kennlebu', 'password', 'Kenneth', 'Lebu', 24)

        # First add the bucket lists and verify that they exist
        user.create_bucketlist("Go to China", datetime.now().strftime('%Y-%m-%d'))
        user.create_bucketlist("Buy an island", datetime.now().strftime('%Y-%m-%d'))
        self.assertEqual(2, len(user.bucketlists), msg='User should have 2 bucketlists')

        # Remove the bucketlists and test whether they have been removed
        user.delete_bucketlist("Go to China")
        self.assertEqual(1, len(user.bucketlists), msg='User should have 1 bucketlist')
        user.delete_bucketlist("Buy an island")
        self.assertEqual(0, len(user.bucketlists), msg='User should have 0 bucketlists')

        # Test removing a bucketlist that does not exist
        user.create_bucketlist("Eat a shark", datetime.now().strftime('%Y-%m-%d'))
        self.assertEqual(user.delete_bucketlist("Eat a snake"), "Bucket list not found",
                         msg="Should return \'Bucket list not found\'")

if __name__ == '__main__':
    unittest.main()
