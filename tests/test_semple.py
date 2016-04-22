import urllib.parse

from app import Application
from tornado.testing import AsyncHTTPTestCase


class TestHello(AsyncHTTPTestCase):
    def get_app(self):
        return Application()

    def test_homepage(self):
        data = urllib.parse.urlencode({'u': 'system', 'r': 'ru-1',
                                       'msg': 'test'})
        data = data.encode('ascii')
        response = self.fetch('/', method='POST', body=data)
        # print(response)
        self.assertEqual(response.code, 200)
