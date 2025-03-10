# coding:utf-8

import os
import unittest

import mock

from xlc.database import DATABASE
from xlc.language import segment
from xlc.language.message import Message


class TestSegment(unittest.TestCase):

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
            cls.root: segment.Segment = segment.Segment.loadf("en.xlc")

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_langtag(self):
        self.assertEqual(self.root.lang.tag, "en")

    def test_get(self):
        self.assertEqual(self.root.lookup("section1").get("key1"), "value1")
        self.assertEqual(self.root.lookup("section2.section3").get("key2"), "value2")  # noqa:E501
        self.assertEqual(self.root.lookup("section2.section3").get("key3"), "value3")  # noqa:E501
        self.assertEqual(self.root.lookup("section2.section3.section4").get("key4"), "value4")  # noqa:E501

    def test_render(self):
        self.assertEqual(self.root.lookup("render").render(value="test"), {"key": "value: test"})  # noqa:E501
        self.assertEqual(self.root.lookup("login").render(username="test", password="1234"),  # noqa:E501
                         {"username": "Username: test", "password": "Password: 1234"})  # noqa:E501


class TestMessage(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.dirname: str = os.path.join(os.path.dirname(__file__), "messages")
        cls.message: Message = Message.load(cls.dirname)

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_iter_and_len(self):
        self.assertEqual(len(self.message), 10)
        for ltag in self.message:
            self.assertIn(ltag, DATABASE.langtags)
        for ltag in DATABASE.langtags:
            if ltag not in self.message:
                continue
            lang = self.message[ltag].lang
            self.assertTrue(lang.tag == ltag or ltag.name in
                            [a.name for a in lang.aliases])

    def test_zh_hans_cn(self):
        self.assertEqual(self.message.lookup("zh-hans-cn").lang.tag, "zh-Hans")

    def test_zh_hant_cn(self):
        self.assertEqual(self.message.lookup("zh-hant-cn").lang.tag, "zh-Hant")

    def test_zh_hans_tw(self):
        self.assertEqual(self.message.lookup("zh-hans-tw").lang.tag, "zh-Hans")

    def test_zh_hant_tw(self):
        self.assertEqual(self.message.lookup("zh-hant-tw").lang.tag, "zh-Hant")

    def test_zh_hans(self):
        self.assertEqual(self.message.lookup("zh-hans").lang.tag, "zh-Hans")

    def test_zh_hant(self):
        self.assertEqual(self.message.lookup("zh-hant").lang.tag, "zh-Hant")

    def test_zh_cn(self):
        self.assertEqual(self.message.lookup("zh-cn").lang.tag, "zh-CN")

    def test_zh_tw(self):
        self.assertEqual(self.message.lookup("zh-tw").lang.tag, "zh-TW")

    def test_lookup_zh(self):
        self.assertRaises(LookupError, self.message.lookup, "zh")


if __name__ == "__main__":
    unittest.main()
