#!/usr/bin/env python
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
dvdprocess command module.

part of the drt package.

Usage:
    dvdprocess
    dvdprocess --help
    dvdprocess -v
    dvdprocess --version
    dvdprocess --allsaved
    dvdprocess -A
    dvdprocess --listsaved
    dvdprocess -l
    dvdprocess --incoming
    dvdprocess -r
    dvdprocess --saved SAVEDNAME ...
    dvdprocess -s SAVEDNAME ...
    dvdprocess --first
    dvdprocess -S

Options:
    -A --allsaved           process all saved DVDs.
    -h --help               this help message.
    -l --listsaved          list all saved DVDs and exit.
    -r --incoming           read the incoming dir. and build the DVD tree for editing. Default action
                            if no options supplied.
    -s --saved SAVEDNAME    process the saved DVD for SAVEDNAME, can be repeated.
    -S --first              process the first saved DVD and exit.
    -v --version            version info.

Notes:
    Process module of drt application

    dvdprocess on it's own will read the incoming directory and start the naming process.

    Reads a copied dvd directory.
    Produces an info file.
    Allows user to name the dvd and assign episode numbers and names to the tracks.
    Allows user to select which tracks to process.
    Allows user to toggle the burning in of subtitles.
    Allows user to save the edited data for processing at a later time.
"""


import logging
import logging.handlers
from docopt import docopt
from drt import __version__
from drt.dvdprocess import DVDProcess


log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
# log.setLevel(logging.DEBUG)

# syslog handler
syslog=logging.handlers.SysLogHandler(address = '/dev/log',
        facility=logging.handlers.SysLogHandler.LOG_DAEMON)
f = logging.Formatter('processDVD: %(message)s')
syslog.setFormatter(f)
log.addHandler(syslog)

# output to terminal
terminal = logging.StreamHandler()
log.addHandler(terminal)


def main():
    args = docopt(__doc__, version=__version__)
    log.debug("{}".format(args))
    dvdp = DVDProcess()
    if args["--allsaved"]:
        # all saved dvds
        dvdp.readSavedDir()
        if len(dvdp.saved) > 0:
            # process them all
            for sdvd in dvdp.saved:
                dvdp.processSaved(sdvd.name)
            dvdp.run()
    elif args["--first"]:
        # first saved dvd
        dvdp.readSavedDir()
        if len(dvdp.saved) > 0:
            dvdp.processSaved(dvdp.saved[0].name)
            dvdp.run()
    elif args["--listsaved"]:
        dvdp.showSaved()
    elif len(args["--saved"]) > 0:
        # selective process of saved dvds
        # docopt appears to have a bug with multiple items, this mitigates it
        # see https://github.com/docopt/docopt/issues/134
        snames = []
        for name in args["--saved"]:
            if name not in snames:
                snames.append(name)
        for sname in snames:
            dvdp.processSaved(sname)
        dvdp.run()
    else:
        # --incoming | -r is the default action
        # read raw dvds
        dvdp.readIncomingDir()
        dvdp.run()

if __name__=="__main__":
    sys.exit(main())
