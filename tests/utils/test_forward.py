from unittest import TestCase
from expkit.utils.forward import MethodForwarder, AttributeForwarder


class SimpleObject(object):
    def __init__(self, some_attribute):
        self.some_attribute = some_attribute


    def no_arg_method(self):
        return self.some_attribute


    def one_arg_method(self, input_object):
        return self.some_attribute, input_object


    def kw_arg_method(self, input_object=None):
        return self.some_attribute, input_object


class AttributeForwarderTest(TestCase):
    INPUT_OBJECT = object()


    def setUp(self):
        self.forwarded_object = SimpleObject(self.INPUT_OBJECT)


    def test_forwards_attribute_take_when_called(self):
        forwarder = AttributeForwarder("some_attribute")

        returned = forwarder(self.forwarded_object)

        self.assertEquals(self.INPUT_OBJECT, returned)


class MethodForwarderTest(TestCase):
    INPUT_OBJECT = object()


    def setUp(self):
        self.forwarded_object = SimpleObject(self.INPUT_OBJECT)


    def test_forwards_no_arg_method_when_called(self):
        forwarder = MethodForwarder("no_arg_method")

        returned = forwarder(self.forwarded_object)

        self.assertEquals(self.INPUT_OBJECT, returned)


    def test_forwards_one_arg_method_when_called_with_arg(self):
        forwarder = MethodForwarder("one_arg_method")

        returned = forwarder(self.forwarded_object, self.INPUT_OBJECT)

        self.assertEquals((self.INPUT_OBJECT, self.INPUT_OBJECT), returned)


    def test_forwards_one_arg_method_when_was_initialised_with_arg(self):
        forwarder = MethodForwarder("one_arg_method", self.INPUT_OBJECT)

        returned = forwarder(self.forwarded_object)

        self.assertEquals((self.INPUT_OBJECT, self.INPUT_OBJECT), returned)


    def test_forwards_kw_arg_method_when_called_with_kw_arg(self):
        forwarder = MethodForwarder("kw_arg_method")

        returned = forwarder(self.forwarded_object, input_object=self.INPUT_OBJECT)

        self.assertEquals((self.INPUT_OBJECT, self.INPUT_OBJECT), returned)


    def test_forwards_kw_arg_method_when_was_initialised_with_kw_arg(self):
        forwarder = MethodForwarder("kw_arg_method", input_object=self.INPUT_OBJECT)

        returned = forwarder(self.forwarded_object)

        self.assertEquals((self.INPUT_OBJECT, self.INPUT_OBJECT), returned)
