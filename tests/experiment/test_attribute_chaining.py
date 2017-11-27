from unittest import TestCase
from expkit.experiment.attribute_chaining import get_chained_attribute, ChainedAttributeError, ChainedAttributeCallForwarder


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


ARBITRARY_VALUE_1 = 42
ARBITRARY_VALUE_2 = 43
ARBITRARY_VALUE_3 = 44


class InnerForwardable(object):
    def inner_method(self, *args):
        return args


    def inner_callable(self):
        return ARBITRARY_VALUE_3


class Forwardable(object):
    def __init__(self):
        self.dict_attribute = {
            "key1": ARBITRARY_VALUE_1,
            "key2": ARBITRARY_VALUE_2
        }
        self.attribute = InnerForwardable()


class ChainedAttributeCallForwarderTest(TestCase):
    def test_can_forward_without_argument(self):
        forwarder = ChainedAttributeCallForwarder(["attribute", "inner_method"])

        result = forwarder(Forwardable())

        self.assertEqual(tuple(), result)


    def test_can_forward_with_single_arbitrary_argument(self):
        forwarder = ChainedAttributeCallForwarder(["attribute", "inner_method"],
                                                  ARBITRARY_VALUE_1)

        result = forwarder(Forwardable())

        self.assertEqual(ARBITRARY_VALUE_1, result[0])


    def test_can_forward_with_single_chained_argument(self):
        forwarder = ChainedAttributeCallForwarder(["attribute", "inner_method"],
                                                  ["dict_attribute", "key1"])

        result = forwarder(Forwardable())

        self.assertEqual(ARBITRARY_VALUE_1, result[0])


    def test_can_forward_with_2_chained_arguments(self):
        forwarder = ChainedAttributeCallForwarder(["attribute", "inner_method"],
                                                  ["dict_attribute", "key1"],
                                                  ["dict_attribute", "key2"])

        result1, result2 = forwarder(Forwardable())

        self.assertEqual(ARBITRARY_VALUE_1, result1)
        self.assertEqual(ARBITRARY_VALUE_2, result2)


    def test_a_non_chained_argument_is_called_if_callable(self):
        forwarder = ChainedAttributeCallForwarder(["attribute", "inner_method"],
                                                  lambda: ARBITRARY_VALUE_3)

        result = forwarder(Forwardable())

        self.assertEqual(ARBITRARY_VALUE_3, result[0])


    def test_a_chained_argument_is_called_if_callable(self):
        forwarder = ChainedAttributeCallForwarder(["attribute", "inner_method"],
                                                  ["attribute", "inner_callable"])

        result = forwarder(Forwardable())

        self.assertEqual(ARBITRARY_VALUE_3, result[0])
