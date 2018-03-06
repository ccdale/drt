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
        if not self.dirExists(pn):
            p = Path(pn)
            ret = False
            try:
                p.mkdir(mode=0o755, parents=True, exist_ok=True)
                ret = True
            except Exception as e:
                print("an error occurred making the path {}, exception was {}".format(pn, e))
        else:
            ret = True
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

    def makeConfigDirs(self, cfg, cfgnames):
        for key in cfgnames:
            self.makePath(cfg[key])

    def rename(self, src, dest):
        p = Path(src)
        p.rename(dest)

    def askMe(self, q, default):
        ret = default
        val = input("{} ({}) > ".format(q, default))
        if len(val) > 0:
            ret = val
        return ret
