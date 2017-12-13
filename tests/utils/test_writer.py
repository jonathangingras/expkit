from unittest import TestCase
from expkit.utils.writer import Writer, SkipWriter, DotWriter, TeeWriter


class StdOutStub(object):
    def __init__(self):
        self.received = ""

    def write(self, arg):
        self.received += arg
        return len(arg)


class NonStrStub(object):
    def __init__(self, str_equivalent):
        self.str_equivalent = str_equivalent
        self.call_count = 0


    def __str__(self):
        self.call_count += 1
        return self.str_equivalent


class WriterTest(TestCase):
    STR = "somestring"
    SEPARATOR = ','


    def setUp(self):
        self.output = StdOutStub()
        self.writer = Writer(output=self.output, separator=self.SEPARATOR)
        self.NONSTR = NonStrStub(self.STR)


    def test_write_writes_a_string_as_is_and_returns_length(self):
        length = self.writer.write(self.STR)

        self.assertEqual(len(self.STR), length)
        self.assertEqual(self.STR, self.output.received)


    def test_write_writes_multiple_strings_separated_by_separator_and_returns_total_length(self):
        length = self.writer.write(self.STR, self.STR)

        self.assertEqual(2 * len(self.STR) + 1, length)
        self.assertEqual(self.STR + self.SEPARATOR + self.STR, self.output.received)


    def test_write_writes_multiple_non_strings_as_strings_separated_by_separator_and_returns_total_length(self):
        length = self.writer.write(self.NONSTR, self.NONSTR)

        self.assertEqual(2 * len(self.STR) + 1, length)
        self.assertEqual(self.STR + self.SEPARATOR + self.STR, self.output.received)
        self.assertEqual(2, self.NONSTR.call_count)


class SkipWriterTest(TestCase):
    SKIP_FACTOR = 10
    STR = "somestring"


    def setUp(self):
        self.output = StdOutStub()
        self.writer = SkipWriter(skip_factor=self.SKIP_FACTOR,
                                 output=self.output)


    def test_writer_writes_only_given_argument_every_skip_factor_time_it_is_called(self):
        length = 0

        for _ in range(self.SKIP_FACTOR + 1):
            length += self.writer.write(self.STR)

        self.assertEqual(2 * len(self.STR), length)
        self.assertEqual(self.STR + self.STR, self.output.received)


class DotWriterTest(TestCase):
    STR = "somestring"
    INSTANCE_TIME_STR = '.'


    def setUp(self):
        self.output = StdOutStub()
        self.writer = DotWriter(string=self.INSTANCE_TIME_STR, output=self.output)


    def test_writer_writes_the_instantiation_time_given_string_instead_of_passed_object(self):
        length = self.writer.write(self.STR)

        self.assertEqual(len(self.INSTANCE_TIME_STR), length)
        self.assertEqual(self.INSTANCE_TIME_STR, self.output.received)


class TeeWriterTest(TestCase):
    STR = "somestring"


    def setUp(self):
        self.output1 = StdOutStub()
        self.output2 = StdOutStub()
        self.writer = TeeWriter(self.output1, self.output2)


    def test_writer_writes_equally_to_both_outputs(self):
        length = self.writer.write(self.STR)

        self.assertEqual(2 * len(self.STR), length)
        self.assertEqual(self.STR, self.output1.received)
        self.assertEqual(self.STR, self.output2.received)
