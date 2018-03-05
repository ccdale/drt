"""
configfile reader/writer for drt application
"""

import yaml
from drt.filesystem import FileSystem
import logging

log = logging.getLogger(__name__)

class ConfigFile(object):
    def __init__(self):
        defaultcfg = {
                "device": "/dev/sr0",
                "rootdir": "~/Videos/dvd",
                "handbrake": "/usr/bin/HandBrakeCLI",
                "dvdbackup": "/usr/bin/dvdbackup",
                "eject": "/usr/bin/eject"
                }
        defaultnames = {
                "dvdoutput": "output",
                "outputdir": "incoming",
                "tmpdir": "bare",
                "completeddir": "processed",
                "saveddir": "saved"
                }
        fs = FileSystem()
        self.cfgfn = fs.absPath("~/.config/drt.yaml")
        if fs.fileExists(self.cfgfn):
            self.readConfig()
        else:
            self.cfg = defaultcfg
            log.debug("writing out config file {}".format(self.cfgfn))
            self.writeConfig()
        self.cfg["rootdir"] = fs.absPath(self.cfg["rootdir"])
        keys = ["outputdir", "tmpdir", "dvdoutput", "completeddir", "saveddir"]
        for key in keys:
            if key not in self.cfg:
                self.cfg[key] = self.cfg["rootdir"] + "/{}".format(defaultnames[key])
            else:
                tmp = fs.absPath(self.cfg[key])
                self.cfg[key] = tmp

    def findConfig(self, searchfns):
        fs = FileSystem()
        found = None
        for fn in searchfns:
            if fs.fileExists(fn):
                found = fn
                break;
        return found

    def readConfig(self):
        try:
            with open(self.cfgfn, 'r') as ymlfn:
                self.cfg = yaml.load(ymlfn)
            self.OK = True
        except Exception as e:
            log.error("An error occurred reading config file {}, exception was {}".format(self.cfgfn, e))

    def writeConfig(self):
        fs = FileSystem()
        fs.makePath(self.cfgfn)
        try:
            with open(self.cfgfn, "w") as ymlfn:
                yaml.dump(self.cfg, ymlfn)
        except Exception as e:
            log.error("An error occurred writing config file {}, exception was {}".format(self.cfgfn, e))

    def getCfg(self):
        return self.cfg
