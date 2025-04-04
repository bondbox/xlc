# coding:utf-8

import unittest

from xlc.database.langtags import LangTag
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


class TestLangTag(unittest.TestCase):

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

    def test_zh_hans_cn(self):
        zh_hans_cn = LangTag("zh-Hans-CN")
        self.assertEqual(str(zh_hans_cn), "zh-Hans-CN")
        tags = [tag for tag in zh_hans_cn]
        self.assertEqual(tags, ["zh-Hans", "zh-CN", "zh"])

    def test_en_us(self):
        en_us = LangTag("en-us")
        self.assertEqual(str(en_us), "en-US")
        tags = [tag for tag in en_us]
        self.assertEqual(tags, ["en"])


class TestLangTags(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.langtags: LangTags = LangTags.from_config()

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_iter_and_len(self):
        self.assertEqual(len([tag for tag in self.langtags]), len(self.langtags))  # noqa:E501

    def test_lookup_aa(self):
        self.assertRaises(LookupError, self.langtags.lookup, "aa")

    def test_lookup_zh_hans_cn(self):
        zh_hans_cn = self.langtags.lookup("zh-Hans-CN")
        self.assertEqual(zh_hans_cn.name, "zh-Hans-CN")
        self.assertEqual(zh_hans_cn.recognition, "简体中文（中国）")
        self.assertEqual(zh_hans_cn.description, "PRC Mainland Chinese in simplified script")  # noqa:E501
        self.assertEqual(str(zh_hans_cn), "zh-Hans-CN(PRC Mainland Chinese in simplified script)")  # noqa:E501

    def test_lookup_zh_hans_us(self):
        zh_hans_us = self.langtags.lookup("zh-Hans-US")
        self.assertEqual(zh_hans_us.name, "zh-Hans")
        self.assertEqual(zh_hans_us.recognition, "简体中文")
        self.assertEqual(zh_hans_us.description, "simplified Chinese")
        self.assertEqual(str(zh_hans_us), "zh-Hans(simplified Chinese)")

    def test_lookup_zh_cn(self):
        zh_cn = self.langtags.lookup("zh-CN")
        self.assertEqual(zh_cn.name, "zh-CN")
        self.assertEqual(zh_cn.recognition, "中文（中国）")
        self.assertEqual(zh_cn.description, "simplified Chinese")
        self.assertEqual(str(zh_cn), "zh-CN(simplified Chinese)")

    def test_lookup_zh_us(self):
        zh_us = self.langtags.lookup("zh-US")
        self.assertEqual(zh_us.name, "zh")
        self.assertEqual(zh_us.recognition, "中文")
        self.assertEqual(zh_us.description, "Chinese")
        self.assertEqual(str(zh_us), "zh(Chinese)")

    def test_lookup_zh_hant(self):
        zh_hant = self.langtags.lookup("zh-Hant")
        self.assertEqual(zh_hant.name, "zh-Hant")
        self.assertEqual(zh_hant.recognition, "繁體中文")
        self.assertEqual(zh_hant.description, "traditional Chinese")
        self.assertEqual(str(zh_hant), "zh-Hant(traditional Chinese)")


if __name__ == "__main__":
    unittest.main()
