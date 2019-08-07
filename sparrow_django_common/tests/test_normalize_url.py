import unittest

from sparrow_django_common.utils.normalize_url import NormalizeUrl


class TestURLSplicing(unittest.TestCase):
    """测试url拼接"""

    def setUp(self):
        self.normalize_url = NormalizeUrl()
        self.scheme_domain = 'http://d.com'
        self.domain = 'd.com'
        self.path = '/search'
        self.url = 'http://d.com/search'

    def test_url_splicing(self):
        """测试"""
        url = self.normalize_url.normalize_url(domain=self.domain, path=self.path)
        self.assertEqual(url, self.url)

    def test_scheme_url_splicing(self):
        scheme_url = self.normalize_url.normalize_url(domain=self.scheme_domain, path=self.path)
        self.assertEqual(scheme_url, self.url)


if __name__ == '__main__':
    unittest.main()

