# coding:utf-8

import unittest

import mock

from xlc.language import segment


class TestContent(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.data = """
[section1]
key1 = "value1"

[section2.section3]
key2 = "value2"
key3 = "value3"

[section2.section3.section4]
key4 = "value4"

[render]
key = "value: {value}"

[login]
username = "Username: {username}"
password = "Password: {password}"
"""
        with mock.patch.object(segment, "open", mock.mock_open(read_data=cls.data)):  # noqa:E501
            cls.root: segment.Segment = segment.Segment.loadf("test.xlc")

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get(self):
        self.assertEqual(self.root.lookup("section1").get("key1"), "value1")
        self.assertEqual(self.root.lookup("section2.section3").get("key2"), "value2")  # noqa:E501
        self.assertEqual(self.root.lookup("section2.section3").get("key3"), "value3")  # noqa:E501
        self.assertEqual(self.root.lookup("section2.section3.section4").get("key4"), "value4")  # noqa:E501

    def test_render(self):
        self.assertEqual(self.root.lookup("render").render(value="test"), {"key": "value: test"})  # noqa:E501
        self.assertEqual(self.root.lookup("login").render(username="test", password="1234"),  # noqa:E501
                         {"username": "Username: test", "password": "Password: 1234"})  # noqa:E501


if __name__ == "__main__":
    unittest.main()
