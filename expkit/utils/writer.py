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
