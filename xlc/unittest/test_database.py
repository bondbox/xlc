# coding:utf-8

import unittest

from xlc.database.langtags import LangTags
from xlc.database.subtags import Language
from xlc.database.subtags import Region
from xlc.database.subtags import Script


class TestSubTags(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_language_ValueError(self):
        self.assertRaises(ValueError, Language.get, "xx")

    def test_language_zh(self):
        language = Language.get("zh")
        self.assertIsInstance(language, Language)
        self.assertEqual(language.code, "zh")
        self.assertEqual(language.name, "Chinese")
        self.assertEqual(language.alpha_2, "zh")
        self.assertEqual(language.alpha_3, "zho")

    def test_script_ValueError(self):
        self.assertRaises(ValueError, Script.get, "xxxx")

    def test_script_hans(self):
        script = Script.get("hans")
        self.assertIsInstance(script, Script)
        self.assertEqual(script.code, "Hans")
        self.assertEqual(script.name, "Han (Simplified variant)")
        self.assertEqual(script.numeric, 501)
        self.assertEqual(script.alpha_4, "Hans")

    def test_region_ValueError(self):
        self.assertRaises(ValueError, Region.get, "xx")

    def test_region_cn(self):
        region = Region.get("cn")
        self.assertIsInstance(region, Region)
        self.assertEqual(region.code, "CN")
        self.assertEqual(region.flag, "🇨🇳")
        self.assertEqual(region.name, "China")
        self.assertEqual(region.numeric, 156)
        self.assertEqual(region.alpha_2, "CN")
        self.assertEqual(region.alpha_3, "CHN")
        self.assertEqual(region.official_name, "People's Republic of China")


class TestLangTags(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.langtags = LangTags()

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_lookup(self):
        self.langtags.lookup("zh-Hans-CN")
        self.langtags.lookup("zh-Hans-US")


if __name__ == "__main__":
    unittest.main()
