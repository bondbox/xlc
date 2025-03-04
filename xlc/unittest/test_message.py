# coding:utf-8

import unittest

from xlc.message import Section


class TestContent(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.title = "hello"
        cls.value = {
            "text": "hello world"
        }
        cls.datas = Section(cls.title, cls.value)

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_attr(self):
        self.assertEqual(self.datas.text, "hello world")

    def test_title(self):
        self.assertEqual(self.datas.title, self.title)
