import sys


class Writer(object):
    def __init__(self, output=sys.stdout, separator=' '):
        self.separator = separator
        self.output = output


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
