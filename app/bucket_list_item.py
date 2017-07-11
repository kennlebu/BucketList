from datetime import datetime

class BucketListItem():
    """ An item in a BucketList """

    def __init__(self, item_name, bucket_list_name):
        self.item_name = item_name
        self.bucket_list_name = bucket_list_name
        self.date_added = datetime.now().strftime('%Y-%m-%d')
