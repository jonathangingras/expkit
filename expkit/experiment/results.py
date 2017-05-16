import os
import glob

def find_result_pickles(dirpath):
    return glob.glob(os.path.join(dirpath, "*.pkl"))
