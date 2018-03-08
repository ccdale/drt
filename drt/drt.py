#!/usr/bin/env python3
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

import os
import sys
import logging
import logging.handlers
from drt.configfile import ConfigFile
from drt.filesystem import FileSystem

log = logging.getLogger(__name__)
# log.setLevel(logging.INFO)
log.setLevel(logging.DEBUG)
# syslog handler
syslog=logging.handlers.SysLogHandler(address = '/dev/log',
        facility=logging.handlers.SysLogHandler.LOG_DAEMON)
f = logging.Formatter('CopyDVD: %(message)s')
syslog.setFormatter(f)
# output to terminal
terminal = logging.StreamHandler()
log.addHandler(syslog)
log.addHandler(terminal)

def copydvd(dvdbackup, dvddevice, cpdir, dvdname):
    cmd = "{} -i {} -o {} -M -n {}".format(dvdbackup, dvddevice, cpdir, dvdname)
    log.debug(cmd)
    ecode = os.system(cmd)
    return ecode

def main():
    exitcode = 1
    cfgfn = ConfigFile()
    cfg = cfgfn.getCfg()
    srcdev=cfg["device"]
    log.debug("src device: {}".format(srcdev))
    outputdir = cfg["outputdir"]
    fs = FileSystem()
    tmpdir = cfg["tmpdir"]
    if len(sys.argv) > 1:
        dvdname = os.path.basename(sys.argv[1].replace(" ", "_"))
    else:
        dvdname = "DVD"
    tmp = fs.askMe("Dvd Name", dvdname)
    if len(tmp) > 0:
        dvdname = tmp
    log.info("Copying dvd {} to {}".format(dvdname, tmpdir))
    exitcode = copydvd(cfg["dvdbackup"], cfg["device"], tmpdir, dvdname)
    if exitcode != 0:
        log.error("error copying dvd, sorry")
        fs.askMe("exit", "")
    else:
        tmpname = tmpdir + "/" + dvdname
        newname = outputdir + "/" + dvdname
        log.info("Moving dvd to output dir")
        fs.rename(tmpname, newname)
    log.info("CopyDVD: ejecting disc.")
    os.system("{} {}".format(cfg["eject"], cfg["device"]))
    return exitcode

if __name__=="__main__":
    sys.exit(main())
