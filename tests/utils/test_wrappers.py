from unittest import TestCase
from expkit.utils.wrappers import LearnerWrapper, is_wrapper, unwrapped


class SomeWrapper(LearnerWrapper):
    def __init__(self):
        self.wrapped = 1

class NonDefaultWrapper(LearnerWrapper):
    def __init__(self):
        self.nondefault = 1

    def __wrapped__(self):
        return self.nondefault

class SomeNonWrapper:
    pass


class WrapperTest(TestCase):
    def test_is_wrapper_returns_true_when_Wrapper_subclass(self):
        obj = SomeWrapper()

        self.assertTrue(is_wrapper(obj))

    def test_is_wrapper_returns_false_when_not_defining_Wrapper_interface(self):
        obj = SomeNonWrapper()

        self.assertFalse(is_wrapper(obj))

    def test_unwrapped_returns_wrapped_when_default_attribute_name(self):
        obj = SomeWrapper()

        self.assertEqual(1, unwrapped(obj))

    def test_unwrapped_returns_wrapped_when_non_default_attribute_name(self):
        obj = NonDefaultWrapper()

        self.assertEqual(1, unwrapped(obj))
