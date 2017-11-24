from unittest import TestCase
from expkit.experiment.before import get_chained_attribute


CHAIN_END = 42


class SomeOneLevelClass(object):
    def __init__(self):
        self.lvl1_attribute = CHAIN_END
        self.lvl1_dict = {"key": CHAIN_END}


class SomeTwoLevelClass(object):
    def __init__(self):
        self.lvl2_attribute = SomeOneLevelClass()


class GetChainedAttributeTest(TestCase):
    def test_can_chain_1_level_attribute(self):
        obj = SomeOneLevelClass()

        chain_end, previous = get_chained_attribute(obj, ["lvl1_attribute"])

        self.assertEqual(CHAIN_END, chain_end)
        self.assertEqual(obj, previous)


    def test_can_chain_2_level_attribute(self):
        obj = SomeTwoLevelClass()

        chain_end, previous = get_chained_attribute(obj, ["lvl2_attribute", "lvl1_attribute"])

        self.assertEqual(CHAIN_END, chain_end)
        self.assertEqual(obj.lvl2_attribute, previous)


    def test_can_chain_1_level_dict_keys_value(self):
        obj = SomeOneLevelClass()

        chain_end, previous = get_chained_attribute(obj, ["lvl1_dict", "key"])

        self.assertEqual(CHAIN_END, chain_end)
        self.assertEqual(obj.lvl1_dict, previous)


    def test_can_chain_2_level_dict_keys_value(self):
        obj = SomeTwoLevelClass()

        chain_end, previous = get_chained_attribute(obj, ["lvl2_attribute", "lvl1_dict", "key"])

        self.assertEqual(CHAIN_END, chain_end)
        self.assertEqual(obj.lvl2_attribute.lvl1_dict, previous)
