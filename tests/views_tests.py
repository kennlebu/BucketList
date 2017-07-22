import unittest
import app.views
from app.user import User
from flask import url_for, Response
import requests

class ViewsTests(unittest.TestCase):
    """ Contains tests for the views """

    view = app.views

    def test_index_redirect(self):
        """ Tests whether going to index without logging in redirects to the login page """

        with app.app.test_request_context():
            self.assertEqual(app.views.index().status_code, 302)
            self.assertEqual(app.views.index().location, url_for('blueprint.login'))

    def test_logout(self):
        """ Tests whether the loguot loads and redirects to login """

        with app.app.test_request_context():
            self.assertEqual(app.views.logout().status_code, 302)
            self.assertEqual(app.views.logout().location, url_for('blueprint.login'))

    def test_view_bucketlist(self):
        """ Tests whether page for viewing a bucketlist loads """

        with app.app.test_client() as client:
            res = client.get('/item?type=new')
            self.assertEqual(res.location().status_code, 200)

if __name__ == '__main__':
    unittest.main()
