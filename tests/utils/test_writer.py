from unittest import TestCase
from expkit.utils.writer import Writer, SkipWriter, DotWriter, TeeWriter, BufferArray, InMemoryWriter, FileWriter
import os
import tempfile
import glob
import uuid


class StdOutStub(object):
    def __init__(self):
        self.received = ""


    def write(self, *args):
        length = 0
        for arg in args:
            self.received += arg
            length += len(arg)
        return length


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


class BufferArrayTest(TestCase):
    STR1 = "somestring1"
    STR2 = "somestring2"
    STR3 = "somestring3"


    def setUp(self):
        self.buffer_array = BufferArray()
        self.output = StdOutStub()


    def test_can_write_an_object_and_see_it_after_dump(self):
        self.buffer_array.write(self.STR1)

        self.buffer_array.dump(self.output)
        self.assertEqual(self.STR1, self.output.received)


    def test_can_write_multiple_objects_and_see_them_after_dump_in_same_order(self):
        self.buffer_array.write(self.STR1)
        self.buffer_array.write(self.STR2)
        self.buffer_array.write(self.STR3)

        self.buffer_array.dump(self.output)
        self.assertEqual(self.STR1 + self.STR2 + self.STR3, self.output.received)


    def test_clear_clears_effectively_buffer_array(self):
        self.buffer_array.write(self.STR1)
        self.buffer_array.write(self.STR2)
        self.buffer_array.write(self.STR3)

        self.buffer_array.clear()

        self.buffer_array.dump(self.output)
        self.assertEqual("", self.output.received)


    def test_len_is_zero_when_empty(self):
        self.assertEqual(0, len(self.buffer_array))


    def test_len_measures_total_data_size_in_str_len_unit(self):
        self.buffer_array.write(self.STR1)
        self.buffer_array.write(self.STR2)
        self.buffer_array.write(self.STR3)

        self.assertEqual(len(self.STR1 + self.STR2 + self.STR3), len(self.buffer_array))


class InMemoryWriterTest(TestCase):
    STR1 = "somestring1"
    STR2 = "somestring2"
    STR3 = "somestring3"


    def setUp(self):
        self.writer = InMemoryWriter()
        self.output = StdOutStub()


    def test_dump_dumps_all_it_was_written_in_same_order(self):
        self.writer.write(self.STR1)
        self.writer.write(self.STR2)
        self.writer.write(self.STR3)

        self.writer.dump(self.output)

        self.assertEqual(self.STR1 + self.STR2 + self.STR3, self.output.received)


class FileWriterTest(TestCase):
    STR1 = "somestring1"
    STR2 = "somestring2"
    STR3 = "somestring3"


    def tearDown(self):
        tuple(map(os.remove, glob.glob(os.path.join(tempfile.gettempdir(), "expkit.test.*"))))


    def random_filename(self):
        return os.path.join(tempfile.gettempdir(), "expkit.test." + str(uuid.uuid4()))


    def test_file_content_is_accurate_when_single_write(self):
        filename = self.random_filename()
        writer = FileWriter(filename)

        writer.write(self.STR1)
        writer.flush()

        with open(filename, "r") as f:
            content = f.read()

        self.assertEqual(self.STR1, content)


    def test_file_content_is_accurate_when_multiple_writes(self):
        filename = self.random_filename()
        writer = FileWriter(filename)

        writer.write(self.STR1)
        writer.write(self.STR2)
        writer.write(self.STR3)
        writer.flush()

        with open(filename, "r") as f:
            content = f.read()

        self.assertEqual(self.STR1 + self.STR2 + self.STR3, content)


    def test_file_content_is_accurate_when_trepassing_buffer_limit_size_with_single_write(self):
        filename = self.random_filename()
        writer = FileWriter(filename, buffer_size=5)

        writer.write(self.STR1)
        writer.flush()

        with open(filename, "r") as f:
            content = f.read()

        self.assertEqual(self.STR1, content)


    def test_file_content_is_accurate_when_trepassing_buffer_limit_size_with_multiple_writes(self):
        filename = self.random_filename()
        writer = FileWriter(filename, buffer_size=5)

        writer.write(self.STR1)
        writer.write(self.STR2)
        writer.write(self.STR3)
        writer.flush()

        with open(filename, "r") as f:
            content = f.read()

        self.assertEqual(self.STR1 + self.STR2 + self.STR3, content)
