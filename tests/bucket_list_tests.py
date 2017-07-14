import unittest
from app.bucket_list import BucketList
from datetime import datetime

class BucketListTest(unittest.TestCase):
    """ Tests for the Bucket List class """

    def test_bucket_list(self):
        """ Tests for the creation of a bucketlist """

        bucket = BucketList("Visit New York", datetime.now().strftime('%Y-%m-%d'))
        self.assertEqual(bucket.name, "Visit New York", msg='Name should be \'Visit New York\'')
        self.assertEqual(bucket.due_date, datetime.now().strftime('%Y-%m-%d'),
                         msg='Due date should be {}'.format(datetime.now().strftime('%Y-%m-%d')))
        self.assertEqual(bucket.date_added, datetime.now().strftime('%Y-%m-%d'),
                         msg='Due date should be {}'.format(datetime.now().strftime('%Y-%m-%d')))

    def test_add_item(self):
        """ Tests whether an item can be added to a bucketlist """

        bucket = BucketList("Visit New York", datetime.now().strftime('%Y-%m-%d'))
        bucket.add_item("Go to empire state building")
        bucket.add_item("Visit Queens")

        # Test for length of the items list
        self.assertEqual(2, len(bucket.items), msg='bucket should have 2 items')

        # Test for the date of the items in the bucket lists
        for item in bucket.items:
            self.assertEqual(item.date_added, datetime.now().strftime('%Y-%m-%d'),
                             msg='date added should be {}'.format(datetime.now()
                                                                  .strftime('%Y-%m-%d')))

    def test_remove_item(self):
        """ Tests whether items can be removed from the bucket list """

        bucket = BucketList("Visit New York", datetime.now().strftime('%Y-%m-%d'))
        bucket.add_item("Go to empire state building")
        bucket.add_item("Visit Queens")

        # Remove the items and test for length of the list
        bucket.remove_item("Go to empire state building")
        self.assertEqual(1, len(bucket.items), msg='bucket should have one item')
        bucket.remove_item("Visit Queens")
        self.assertEqual(0, len(bucket.items), msg='bucket should have 0 items')

    def test_mark_as_done(self):
        """ Tests whether items can be marked as done """

        bucket = BucketList("Visit New York", datetime.now().strftime('%Y-%m-%d'))
        bucket.add_item("Go to empire state building")
        bucket.add_item("Visit Queens")

        # Mark items as done and test for it
        bucket.mark_item_as_done("Go to empire state building")
        bucket.mark_item_as_done("Visit Queens")
        for item in bucket.items:
            assert item.done

    def test_mark_as_undone(self):
        """ Tests whether items can be marked as undone """

        bucket = BucketList("Visit New York", datetime.now().strftime('%Y-%m-%d'))
        bucket.add_item("Go to empire state building")
        bucket.add_item("Visit Queens")

        # First mark the items as done and test to make sure they are
        bucket.mark_item_as_done("Go to empire state building")
        bucket.mark_item_as_done("Visit Queens")
        for item in bucket.items:
            assert item.done

        # Now mark as undone and test
        bucket.mark_item_as_undone("Go to empire state building")
        bucket.mark_item_as_undone("Visit Queens")
        for item in bucket.items:
            assert not item.done

if __name__ == '__main__':
    unittest.main()
