import sys
from functools import reduce


class StdOutOutput(object):
    def write(self, arg):
        return sys.stdout.write(arg)


class TeeWriter(object):
    def __init__(self, output, tee_output):
        if output is None or tee_output is None:
            raise ValueError("no output may be None")
        self.output = output
        self.tee_output = tee_output


    def write(self, *args):
        return self.output.write(*args) + self.tee_output.write(*args)


class Writer(object):
    def __init__(self, output=None, separator=' '):
        self.separator = separator
        if output is None:
            self.output = StdOutOutput()
        else:
            self.output = output


    def __eq__(self, other):
        if isinstance(other, Writer):
            return self.output == other.output
        return False


    def write(self, *args):
        return self.output.write(self.separator.join(map(str, args)))


class SkipWriter(Writer):
    def __init__(self, output=None, separator=' ', skip_factor=10):
        super().__init__(output=output, separator=separator)
        self.count = 0
        self.skip_factor = skip_factor


    def write(self, *args):
        length = 0
        if self.count % self.skip_factor == 0:
            length = super().write(*args)

        self.count += 1

        return length


class DotWriter(Writer):
    def __init__(self, output=None, separator=' ', string='.'):
        super().__init__(output=output, separator=separator)
        self.string = string


    def write(self, *args):
        return super().write(self.string)


class BufferArray(object):
    def __init__(self):
        self.data = []


    def write(self, arg):
        self.data.append(arg)
        return len(self.data[-1])


    def clear(self):
        self.data.clear()


    def dump(self, output):
        tuple(map(output.write, self.data))


    def __len__(self):
        if len(self.data) == 0:
            return 0
        return reduce(lambda x, y: x + y, map(len, self.data))


    def __repr__(self):
        return "<{}.{} object with data: {}>".format(self.__class__.__module__,
                                                     self.__class__.__name__,
                                                     self.data)


    def __str__(self):
        return "".join(self.data)


    def __format__(self, f):
        return str(self)


class InMemoryWriter(Writer):
    def __init__(self, separator=' '):
        super().__init__(output=BufferArray(), separator=separator)


    def dump(self, output):
        self.output.dump(output)


class FileWriter(Writer):
    def __init__(self, filename, separator=' ', buffer_size=1024):
        super().__init__(output=BufferArray(), separator=separator)
        self.filename = filename
        self.buffer_limit = buffer_size


    def __del__(self):
        self.flush()


    def flush(self):
        with open(self.filename, "a") as f:
            self.output.dump(f)
        self.output.clear()


    def write(self, *args):
        if len(self.output) + 1 > self.buffer_limit:
            self.flush()

        return super().write(*args)
