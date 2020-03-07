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
DVDProcess - process on disk DVDs with HandBrake
"""
import os
import time
import logging
from drt.configfile import ConfigFile
from drt.filesystem import FileSystem
from drt.dvddisc import DVDDisc
from drt.saveddvd import SavedDvd

log = logging.getLogger(__name__)


class DVDProcess(object):
    def __init__(self):
        cfgfn = ConfigFile()
        cfg = cfgfn.getCfg()
        self.fs = FileSystem()
        self.rootdir = cfg["rootdir"]
        self.incomingdir = cfg["outputdir"]
        self.outputdir = cfg["dvdoutput"]
        self.processed = cfg["completeddir"]
        self.dvdsavedir = cfg["saveddir"]
        self.logdir = cfg["logsdir"]
        self.infodir = cfg["infodir"]
        self.handbrake = cfg["handbrake"]
        self.shortlen = cfg["shorttrack"]
        self.preset = cfg["preset"]
        self.dvds = []
        self.saved = []

    def processSaved(self, sname):
        if len(self.saved) == 0:
            self.readSavedDir()
        for saved in self.saved:
            if sname == saved.name:
                saved.dvd.showMe()
                saved.dvd.showTracks()
                self.dvds.append(saved.dvd)
                saved.moveToIncoming()

    def readSavedDir(self):
        with os.scandir(self.dvdsavedir) as pt:
            for item in pt:
                if self.fs.dirExists(item.path):
                    self.saved.append(
                        SavedDvd(item.name, item.path, self.incomingdir, self.processed)
                    )

    def showSaved(self):
        if len(self.saved) == 0:
            self.readSavedDir()
        for saved in self.saved:
            print("{} - {}".format(saved.name, saved.dvd.seriesname))

    def readIncomingDir(self):
        with os.scandir(self.incomingdir) as pt:
            for item in pt:
                dvd = DVDDisc(
                    item.name,
                    item.path,
                    self.infodir,
                    self.outputdir,
                    self.handbrake,
                    self.dvdsavedir,
                    shortlen=self.shortlen,
                    preset=self.preset,
                )
                instone = False
                first = True
                while not instone:
                    dvd.showMe()
                    dvd.showTracks()
                    if first:
                        dvd.editMe()
                        dvd.showMe()
                        dvd.showTracks()
                        first = False
                    val = self.fs.askMe(
                        "edit [d]vd, edit [t]racks, [s]ave, s[k]ip, [o]k", "o"
                    )
                    if len(val) == 0:
                        val = "o"
                    if val == "o":
                        instone = True
                        acn = len(dvd.alltracks)
                        ccn = len(dvd.selected)
                        log.info(
                            "adding DVD: {} with {} tracks, {} of which are selected".format(
                                dvd.name, acn, ccn
                            )
                        )
                        self.dvds.append(dvd)
                    elif val == "d":
                        dvd.editMe()
                    elif val == "t":
                        dvd.edittracks()
                    elif val == "s":
                        dvd.saveMe()
                        instone = True
                    elif val == "k":
                        instone = True
                    else:
                        dvd.editMe()

    def addZero(self, num):
        ret = "{}".format(num)
        if num < 10:
            ret = "0" + ret
        return ret

    def hms(self, secs):
        rem = secs % 3600
        hrs = int(secs / 3600)
        mins = int(rem / 60)
        osecs = rem % 60
        hrs = self.addZero(hrs)
        mins = self.addZero(mins)
        osecs = self.addZero(osecs)
        return "{}:{}:{}".format(hrs, mins, osecs)

    def run(self):
        runstart = int(time.time())
        tdur = 0
        if len(self.dvds) > 0:
            for dvd in self.dvds:
                dtdur = 0
                dstart = int(time.time())
                for trk in dvd.alltracks:
                    if trk.number in dvd.selected:
                        dtdur += trk.dursecs
                        trkstart = int(time.time())
                        dvd.makeMp4(trk)
                        trkstop = int(time.time())
                        trktime = trkstop - trkstart
                        print("track {} took {}".format(trk.number, self.hms(trktime)))
                tdur += dtdur
                dstop = int(time.time())
                dtime = dstop - dstart
                print("dvd {} took {}".format(dvd.name, self.hms(dtime)))
                self.fs.rename(dvd.path, "{}/{}".format(self.processed, dvd.name))
        runstop = int(time.time())
        print("process run took {}".format(self.hms(runstop - runstart)))
