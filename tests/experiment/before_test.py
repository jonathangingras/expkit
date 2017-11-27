from unittest import TestCase
from expkit.experiment.before import get_chained_attribute, ChainedAttributeError


CHAIN_END = 42
METHOD_RETURN = "method return"
NO_SUCH_KEY = "no such key"


class SomeOneLevelClass(object):
    def __init__(self):
        self.lvl1_attribute = CHAIN_END
        self.lvl1_dict = {"key": CHAIN_END}


    def some_method(self):
        return METHOD_RETURN


class SomeTwoLevelClass(object):
    def __init__(self):
        self.lvl2_attribute = SomeOneLevelClass()


class GetChainedAttributeTest(TestCase):
    def test_can_chain_1_level_attribute(self):
        obj = SomeOneLevelClass()

        chain_end = get_chained_attribute(obj, ["lvl1_attribute"])

        self.assertEqual(CHAIN_END, chain_end)


    def test_can_chain_2_level_attribute(self):
        obj = SomeTwoLevelClass()

        chain_end = get_chained_attribute(obj, ["lvl2_attribute", "lvl1_attribute"])

        self.assertEqual(CHAIN_END, chain_end)


    def test_a_missing_attribute_in_chain_fallsback_to_subscript_operator(self):
        obj = SomeOneLevelClass()

        chain_end = get_chained_attribute(obj, ["lvl1_dict", "key"])

        self.assertEqual(CHAIN_END, chain_end)


    def test_a_missing_attribute_in_chain_fallsback_to_subscript_operator_at_lvl2(self):
        obj = SomeTwoLevelClass()

        chain_end = get_chained_attribute(obj, ["lvl2_attribute", "lvl1_dict", "key"])

        self.assertEqual(CHAIN_END, chain_end)


    def test_can_return_a_bound_method(self):
        obj = SomeTwoLevelClass()

        chain_end = get_chained_attribute(obj, ["lvl2_attribute", "some_method"])

        self.assertEqual(obj.lvl2_attribute.some_method, chain_end)
        self.assertEqual(METHOD_RETURN, chain_end())


    def test_a_missing_attribute_or_key_raises_chained_attribute_error(self):
        obj = SomeTwoLevelClass()

        with self.assertRaises(ChainedAttributeError):
            get_chained_attribute(obj, ["lvl2_attribute", NO_SUCH_KEY])
