#
# Copyright (c) 2018, Christopher Allison
#
#     This file is part of drt.
#
#     drt is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     drt is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with drt.  If not, see <http://www.gnu.org/licenses/>.
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
            "eject": "/usr/bin/eject",
            "shortrack": 300,
        }
        defaultnames = {
            "dvdoutput": "output",
            "outputdir": "incoming",
            "tmpdir": "bare",
            "completeddir": "processed",
            "saveddir": "saved",
            "infodir": "info",
            "logsdir": "logs",
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
        keys = ["logsdir", "infodir"]
        for key in keys:
            if key not in self.cfg:
                self.cfg[key] = self.cfg["dvdoutput"] + "/{}".format(defaultnames[key])
            else:
                tmp = fs.absPath(self.cfg[key])
                self.cfg[key] = tmp
        cfgnames = ["rootdir"]
        for key in defaultnames:
            cfgnames.append(key)
        fs.makeConfigDirs(self.cfg, cfgnames)

    def findConfig(self, searchfns):
        fs = FileSystem()
        found = None
        for fn in searchfns:
            if fs.fileExists(fn):
                found = fn
                break
        return found

    def readConfig(self):
        try:
            with open(self.cfgfn, "r") as ymlfn:
                self.cfg = yaml.load(ymlfn, Loader=yaml.SafeLoader)
            self.OK = True
        except Exception as e:
            log.error(
                "An error occurred reading config file {}, exception was {}".format(
                    self.cfgfn, e
                )
            )

    def writeConfig(self):
        fs = FileSystem()
        fs.makePath(self.cfgfn)
        try:
            with open(self.cfgfn, "w") as ymlfn:
                yaml.dump(self.cfg, ymlfn)
        except Exception as e:
            log.error(
                "An error occurred writing config file {}, exception was {}".format(
                    self.cfgfn, e
                )
            )

    def getCfg(self):
        return self.cfg
