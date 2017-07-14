from .bucket_list import BucketList

class User:
    """ A user signed up to DaBucketList """

    def __init__(self, username, password, firstname, lastname, age):
        self.username = username
        self.password = password
        self.firstname = firstname
        self.lastname = lastname
        self.age = age
        self.bucketlists = []

    def create_bucketlist(self, name, due_date):
        """ Creates a new bucketlist and adds it to the list of the user's bucketlists """

        self.bucketlists.append(BucketList(name, due_date))

    def delete_bucketlist(self, name):
        """ Deletes a bucket list """

        found = False
        for item in self.bucketlists:
            if item.name == name:
                self.bucketlists.remove(item)
                found = True

        if not found:
            return "Bucket list not found"
        else:
            return "Bucket list deleted"
