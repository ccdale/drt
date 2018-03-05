"""
filesystem routines
"""
import os
from pathlib import Path

class FileNotFound(Exception):
    pass

class DirNotFound(Exception):
    pass

class FileSystem(object):
    def fileExists(self, fn):
        if len(fn):
            p = Path(fn)
            return p.is_file()
        else:
            return False

    def dirExists(self, dn):
        d = Path(dn)
        if len(dn):
            return d.is_dir()
        else:
            return False

    def makePath(self, pn):
        p = Path(pn)
        ret = False
        try:
            p.mkdir(mode=0o755, parents=True, exist_ok=True)
            ret = True
        except Exception as e:
            print("an error occurred making the path {}, exception was {}".format(pn, e))
        return ret

    def makeFilePath(self, fn):
        ret = False
        try:
            pfn = os.path.basename(fn)
            self.makePath(pfn)
            ret = True
        except Exception as e:
            print("an error occurred making file path {}, exception was {}".format(fn, e))
        return ret

    def absPath(self, fn):
        return os.path.abspath(os.path.expanduser(fn))
