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
        fs = FileSystem()
        self.incomingdir = fs.absPath(cfg["outputdir"])
        self.outputdir = fs.absPath(cfg["dvdoutput"])
        self.processed = fs.absPath(cfg["completeddir"])
        self.dvdsavedir = fs.absPath(cfg["saveddir"])
        self.logdir = os.path.join(self.outputdir, "logs")
        self.infodir = os.path.join(self.outputdir, "info")
        self.handbrake = cfg["handbrake"]
        self.dvds = []
        self.saved = []

    # def loadOrRead(self):
    #     val = self.askMe("(l)oad saved DVDs or (r)ead new", "r")
    #     if len(val) == 0:
    #         self.readIncomingDir()
    #     elif val == "r":
    #         self.readIncomingDir()
    #     elif val == "l":
    #         self.loadSaved()

    def processSaved(self, sname):
        if len(self.saved) == 0:
            self.readSavedDir()
        for saved in self.saved:
            if sname == saved.name:
                saved.dvd.showMe()
                saved.dvd.showTracks()
                self.dvds.append(saved.dvd)
                saved.moveToIncoming()

    # def loadSaved(self):
    #     self.readSavedDir()
    #     self.showSaved()
    #     dval = self.askMe("Enter the name of the DVD to process", "{}".format(self.saved[0].name))
    #     if len(dval) == 0:
    #         dname = self.saved[0].name
    #     else:
    #         dname = dval
    #     for saved in self.saved:
    #         if saved.name == dname:
    #             saved.dvd.showMe()
    #             saved.dvd.showTracks()
    #             self.dvds.append(saved.dvd)
    #             os.rename(saved.path, "{}/{}".format(self.incomingdir, saved.name))
    #             os.rename(saved.pickled, "{}/{}".format(self.processed, os.path.basename(saved.pickled)))

    def readSavedDir(self):
        with os.scandir(self.dvdsavedir) as pt:
            for item in pt:
                if os.path.isdir(item.path):
                    self.saved.append(SavedDvd(item.name, item.path, self.incomingdir, self.processed))

    def showSaved(self):
        if len(self.saved) == 0:
            self.readSavedDir()
        for saved in self.saved:
            print("{} - {}".format(saved.name, saved.dvd.seriesname))

    def readIncomingDir(self):
        with os.scandir(self.incomingdir) as pt:
            for item in pt:
                dvd = DVDDisc(item.name, item.path, self.infodir, self.outputdir, self.handbrake, self.dvdsavedir)
                instone = False
                while not instone:
                    dvd.showMe()
                    dvd.showTracks()
                    val = self.askMe("edit [d]vd, edit [t]racks, [s]ave, s[k]ip, [o]k", "o")
                    if len(val) == 0:
                        val="o"
                    if val == "o":
                        instone = True
                        acn = len(dvd.alltracks)
                        ccn = len(dvd.selected)
                        log.info("adding DVD: {} with {} tracks, {} of which are selected".format(dvd.name, acn, ccn))
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


    def askMe(self, q, default):
        ret = default
        val = input("{} ({}) > ".format(q, default))
        if len(val) > 0:
            ret = val
        return ret

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
        hrs = addZero(hrs)
        mins = addZero(mins)
        osecs = addZero(osecs)
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
                        pc = (trk.dursecs / trktime) * 100
                        print("track {} took {} ({}) {}% speedup".format(trk.number, self.hms(trk.time), trk.duration, pc))
                tdur += dtdur
                dstop = int(time.time())
                dtime = dstop - dstart
                print("dvd {} took {}".format(dvd.name, self.hms(dtime)))
                os.rename(dvd.path, "{}/{}".format(self.processed, dvd.name))
        runstop = int(time.time())
        print("process run took {}".format(self.hms(runstop - runstart)))
