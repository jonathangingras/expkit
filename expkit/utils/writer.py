import sys
from functools import reduce


class StdOutOutput(object):
    def write(self, arg):
        return sys.stdout.write(arg)


class Writer(object):
    def __init__(self, output=StdOutOutput(), separator=' '):
        self.separator = separator
        self.output = output


    def __eq__(self, other):
        if isinstance(other, Writer):
            return self.output == other.output
        return False


    def write(self, *args):
        return self.output.write(self.separator.join(map(str, args)))


class SkipWriter(Writer):
    def __init__(self, skip_factor=10, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.count = 0
        self.skip_factor = skip_factor


    def write(self, *args):
        length = 0
        if self.count % self.skip_factor == 0:
            length = super().write(*args)

        self.count += 1

        return length


class DotWriter(Writer):
    def __init__(self, string='.', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.string = string


    def write(self, *args):
        return super().write(self.string)


class TeeWriter(Writer):
    def __init__(self, output, tee_output, *args, **kwargs):
        super().__init__(output=output, *args, **kwargs)
        self.tee_output = tee_output


    def write(self, *args):
        return super().write(*args) + self.tee_output.write(*args)


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
    def __init__(self, *args, **kwargs):
        super().__init__(output=BufferArray(), *args, **kwargs)


    def dump(self, output):
        self.output.dump(output)


class FileWriter(Writer):
    def __init__(self, filename, *args, buffer_size=1024, **kwargs):
        super().__init__(output=BufferArray(), *args, **kwargs)
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
