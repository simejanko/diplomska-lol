import cPickle
from collections import *
import os
import zipfile

file_cache = OrderedDict()

def save_obj(obj, filename ):
    with open(filename, 'wb') as f:
        cPickle.dump(obj, f, cPickle.HIGHEST_PROTOCOL)

def load_obj(filename):
    pkl_filename = filename[:-3] + 'pkl'

    if pkl_filename in file_cache:
        return file_cache[pkl_filename]

    if not os.path.isfile(pkl_filename):
        with zipfile.ZipFile(filename) as myzip:
            myzip.extractall('data/')

    with open(pkl_filename, 'rb') as f:
        try:
            file_cache[pkl_filename] = cPickle.load(f)
        except EOFError:
            return False
        if len(file_cache)>2:
            file_cache.popitem(last=False)
        return file_cache[pkl_filename]

