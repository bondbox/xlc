# coding:utf-8

import os
import unittest
from unittest import mock

from xlc.database import LANGTAGS
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
            self.assertIn(ltag, LANGTAGS)
        for ltag in LANGTAGS:
            if ltag not in self.message:
                continue
            lang = self.message[ltag].lang
            self.assertTrue(lang.tag == ltag or ltag.name in
                            [a.name for a in lang.aliases])

    def test_zh_hans_cn(self):
        zh_hans_cn = self.message.lookup("zh-hans-cn")
        self.assertEqual(zh_hans_cn.lang.tag, "zh-Hans")
        self.assertEqual(zh_hans_cn.lang.recognition, "简体中文")

    def test_zh_hant_cn(self):
        zh_hant_cn = self.message.lookup("zh-hant-cn")
        self.assertEqual(zh_hant_cn.lang.tag, "zh-Hant")
        self.assertEqual(zh_hant_cn.lang.recognition, "繁體中文")

    def test_zh_hans_tw(self):
        zh_hans_tw = self.message.lookup("zh-hans-tw")
        self.assertEqual(zh_hans_tw.lang.tag, "zh-Hans")
        self.assertEqual(zh_hans_tw.lang.recognition, "简体中文")

    def test_zh_hant_tw(self):
        zh_hant_tw = self.message.lookup("zh-hant-tw")
        self.assertEqual(zh_hant_tw.lang.tag, "zh-Hant")
        self.assertEqual(zh_hant_tw.lang.recognition, "繁體中文")

    def test_zh_hans(self):
        zh_hans = self.message.lookup("zh-hans")
        self.assertEqual(zh_hans.lang.tag, "zh-Hans")
        self.assertEqual(zh_hans.lang.recognition, "简体中文")

    def test_zh_hant(self):
        zh_hant = self.message.lookup("zh-hant")
        self.assertEqual(zh_hant.lang.tag, "zh-Hant")
        self.assertEqual(zh_hant.lang.recognition, "繁體中文")

    def test_zh_cn(self):
        zh_cn = self.message.lookup("zh-cn")
        self.assertEqual(zh_cn.lang.tag, "zh-CN")
        self.assertEqual(zh_cn.lang.recognition, "中文（中国）")

    def test_zh_tw(self):
        zh_tw = self.message.lookup("zh-tw")
        self.assertEqual(zh_tw.lang.tag, "zh-TW")
        self.assertEqual(zh_tw.lang.recognition, "中文（中国台湾）")

    def test_lookup_zh(self):
        self.assertRaises(LookupError, self.message.lookup, "zh")


if __name__ == "__main__":
    unittest.main()
