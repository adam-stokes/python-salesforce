import os
import re
import inspect
import fnmatch
from contextlib import closing
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

class SchemaHelper(object):
    """ Holder class for when we utilize Schema
    """
    pass

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

def import_module(module_fqname, superclasses=None):
    """Imports the module module_fqname and returns a list of defined classes
    from that module. If superclasses is defined then the classes returned will
    be subclasses of the specified superclass or superclasses. If superclasses
    is plural it must be a tuple of classes."""
    module_name = module_fqname.rpartition(".")[-1]
    module = __import__(module_fqname, globals(), locals(), [module_name])
    modules = [class_ for cname, class_ in
               inspect.getmembers(module, inspect.isclass)
               if class_.__module__ == module_fqname]
    if superclasses:
        modules = [m for m in modules if issubclass(m, superclasses)]

    return modules

def import_resource(name, superclasses=None):
    """Import name as a module and return a list of all classes defined in that
    module. superclasses should be a tuple of valid superclasses to import,
    this defaults to (SchemaHelper,).
    """
    res_fqname = "sforce.models.%s" % name
    if not superclasses:
        superclasses = (SchemaHelper,)
    return import_module(res_fqname, superclasses)

class ImporterHelper(object):
    """Provides a list of modules that can be imported in a package.
    Importable modules are located along the module __path__ list and modules
    are files that end in .py
    """

    def __init__(self, package):
        """package is a package module
        import my.package.module
        helper = ImporterHelper(my.package.module)"""
        self.package = package

    def _resource_name(self, path):
        "Returns the resource module name given the path"
        base = os.path.basename(path)
        name, ext = os.path.splitext(base)
        return name

    def _get_resources_from_list(self, list_):
        resources = [self._resource_name(res)
                for res in list_
                if "__init__" not in res
                and res.endswith(".py")]
        resources.sort()
        return resources

    def _find_resources_in_dir(self, path):
        if os.path.exists(path):
            py_files = list(find("*.py", path))
            pnames = self._get_resources_from_list(py_files)
            if pnames:
                return pnames
            else:
                return []

    def get_modules(self):
        "Returns the list of importable modules in the configured python package."
        resources = []
        for path in self.package.__path__:
            resources.extend(self._find_resources_in_dir(path))
        return resources
