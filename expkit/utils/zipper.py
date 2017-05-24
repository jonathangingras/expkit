from zipfile import ZipFile, ZIP_DEFLATED
import os


class FileZipper(object):
    def __init__(self, zip_filepath):
        self.zipfile = ZipFile(zip_filepath, "w", ZIP_DEFLATED)

    def close(self):
        self.zipfile.close()

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        self.close()

    def __zipfile(self, filepath):
        self.zipfile.write(filepath)

    def __zipdir(self, dirpath):
        for root, dirs, files in os.walk(dirpath):
            for filepath in files:
                self.zipfile.write(os.path.join(root, filepath))

    def zip(self, filepaths, recursive=True):
        if not callable(getattr(filepaths, "__iter__")) or isinstance(filepaths, str):
            filepaths = (filepaths,)

        for filepath in filepaths:
            if os.path.isdir(filepath) and recursive:
                self.__zipdir(filepath)
            else:
                self.__zipfile(filepath)
