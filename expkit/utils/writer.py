import sys


class Writer(object):
    def __init__(self, output=sys.stdout, separator=' '):
        self.separator = separator
        self._output = self.__assert_no_std(output)


    def __eq__(self, other):
        if isinstance(other, Writer):
            return self.output == other.output
        return False


    def __assert_no_std(self, output):
        if output == sys.stdout:
            return 0
        elif output == sys.stderr:
            return 2
        else:
            return output


    @property
    def output(self):
        if self._output == 0:
            return sys.stdout
        elif self._output == 2:
            return sys.stderr
        else:
            return self._output


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
