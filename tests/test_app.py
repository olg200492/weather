import urllib.request
import unittest
from flask import Flask, app
from flask_testing import TestCase
from weather import *

class MyTest(TestCase):

    def create_app(self):

        app = weather()
        app.config['TESTING'] = True
        app.config['LIVESERVER_PORT'] = 0
        return app
    
    def test_server_is_up_and_running(self):
        response = urllib.request.urlopen(self.get_server_url())
        self.assertEqual(response.code, 200)
        
if __name__ == '__main__':
    unittest.main()