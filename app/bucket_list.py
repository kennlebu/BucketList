from datetime import datetime

class BucketList():
    """ Contains the bucket list and the methods used to add and remove items from it """

    def __init__(self, name, due_date):
        self.name = name
        self.date_added = datetime.now().strftime('%Y-%m-%d')
        self.due_date = due_date
        self.items = []

    def add_item(self, item_name):
        """ Adds an item to the bucket list """

        item = {}
        item["item_name"] = item_name
        item["bucket_list_name"] = self.name
        item["date_added"] = datetime.now().strftime('%Y-%m-%d')
        item["done"] = False # Item is marked as not accomplished by default

        # Add the item to the items list in the bucket list
        self.items.append(item)

    def remove_item(self, item_name):
        """ removes an item from the bucket list """

        found = False
        for item in self.items:
            if item["item_name"] == item_name:
                del item["item_name"]
                found = True # Mark the item as found

        if not found:
            return "Item not found"
        else:
            return "Item removed"

    def mark_item_as_done(self, item_name):
        """ Marks a bucketlist item as done """

        found = False
        for item in self.items:
            if item["item_name"] == item_name:
                item["done"] = True
                found = True

        if not found:
            return "Item not found"
        else:
            return "Item removed"

    def mark_item_as_undone(self, item_name):
        """ Marks a bucketlist item as not done """

        found = False
        for item in self.items:
            if item["item_name"] == item_name:
                item["done"] = False
                found = True

        if not found:
            return "Item not found"
        else:
            return "Item removed"
