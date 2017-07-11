import unittest
from app.bucket_list import BucketList
from datetime import datetime
import os, nose, coverage

def main():    
    file_path = os.path.abspath(__file__)
    tests_path = os.path.join(os.path.abspath(os.path.dirname(file_path)), "tests")
    result = nose.run(argv=[os.path.abspath(__file__),
                            "--with-cov", "--verbosity=3", "--cover-package=app", tests_path])

if __name__ == '__main__':
    main()