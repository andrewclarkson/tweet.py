import os
from tweet import app
from unittest import TestCase, main
import tempfile

class HelloTestCase(TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_hello(self):
        res = self.app.get('/')
        assert 'Hello World' in res.data

if __name__ == '__main__':
    main()
