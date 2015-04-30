import os
from tweet import app, db, Tweet
from unittest import TestCase, main
import tempfile

class HelloTestCase(TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        db.connect()
        db.create_tables([Tweet])

    def test_compose_link(self):
        res = self.app.get('/')
        assert 'Compose' in res.data

if __name__ == '__main__':
    main()
