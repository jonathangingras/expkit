import sys


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
        self.data += arg
        return len(arg)


    def clear(self):
        self.data.clear()


    def write_to(self, output):
        tuple(map(output.write, self.data))


    def __len__(self):
        return len(self.data)


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


class FileWriter(Writer):
    def __init__(self, filename, *args, buffer_size=1024, mode="w+", **kwargs):
        super().__init__(*args, **kwargs)
        self.filename = filename
        self.mode = mode
        self.buffer_size = buffer_size
        self.buffer = BufferArray()


    def __del__(self):
        self.flush()


    def flush(self):
        with open(self.filename, self.mode) as f:
            self.buffer.write_to(f)
        self.buffer.clear()


    @property
    def output(self):
        if len(self.buffer) + 1 > self.buffer_size:
            self.flush()

        return self.buffer
