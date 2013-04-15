import os
import re
import fnmatch
from contextlib import closing
from collections import OrderedDict
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

def fileobj(path_or_file, mode='r'):
    """Returns a file-like object that can be used as a context manager"""
    if isinstance(path_or_file, basestring):
        try:
            return open(path_or_file, mode)
        except:
            return closing(StringIO())
    else:
        return closing(path_or_file)

def find(file_pattern, top_dir, max_depth=None, path_pattern=None):
    """generator function to find files recursively. Usage:

    for filename in find("*.properties", "/var/log/foobar"):
    print filename
    """
    if max_depth:
        base_depth = os.path.dirname(top_dir).count(os.path.sep)
        max_depth += base_depth

    for path, dirlist, filelist in os.walk(top_dir):
        if max_depth and path.count(os.path.sep) >= max_depth:
            del dirlist[:]

        if path_pattern and not fnmatch.fnmatch(path, path_pattern):
            continue

        for name in fnmatch.filter(filelist, file_pattern):
            yield os.path.join(path, name)

def grep(pattern, *files_or_paths):
    """Returns lines matched in fnames, where fnames can either be pathnames to files
    to grep through or open file objects to grep through line by line"""
    matches = []

    for fop in files_or_paths:
        with fileobj(fop) as fo:
            matches.extend((line for line in fo if re.match(pattern, line)))

    return matches

# Supports nested dicts
class Struct(object):
    """Comment removed"""
    def __init__(self, data):
        for name, value in data.iteritems():
            setattr(self, name, self._wrap(value))
    def _wrap(self, value):
        if isinstance(value, (tuple, list, set, frozenset)): 
            return type(value)([self._wrap(v) for v in value])
        else:
            return Struct(value) if isinstance(value, dict) else value
    def __getitem__(self, val):
        return self.__dict__[val]
    def __repr__(self):
        return '{%s}' % str(', '.join('%s : %s' % (k, repr(v))\
            for (k, v) in self.__dict__.iteritems()))

# SO: http://stackoverflow.com/a/5227863
class MutableNamedTuple(OrderedDict):
    def __init__(self, *args, **kwargs):
        super(MutableNamedTuple, self).__init__(*args, **kwargs)
        self._initialized = True

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        if hasattr(self, '_initialized'):
            super(MutableNamedTuple, self).__setitem__(name, value)
        else:
            super(MutableNamedTuple, self).__setattr__(name, value)
