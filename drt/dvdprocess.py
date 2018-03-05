"""
DVDProcess - process on disk DVDs with HandBrake
"""
import os
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
        self.rootdir = cfg["rootdir"]
        self.incomingdir = cfg["outputdir"]
        self.outputdir = cfg["dvdoutput"]
        self.processed = cfg["completeddir"]
        self.dvdsavedir = cfg["saveddir"]
        self.logdir = os.path.join(self.outputdir, "logs")
        self.infodir = os.path.join(self.outputdir, "info")
        self.makeDirs()
        self.handbrake = cfg["handbrake"]
        self.dvds = []
        self.saved = []

    def makeDirs(self):
        self.makeDir(self.rootdir)
        self.makeDir(self.incomingdir)
        self.makeDir(self.outputdir)
        self.makeDir(self.processed)
        self.makeDir(self.dvdsavedir)
        self.makeDir(self.logdir)
        self.makeDir(self.infodir)

    def makeDir(self, dir):
        if not os.path.isdir(dir):
            os.mkdir(dir, 0o750)

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

    def run(self):
        if len(self.dvds) > 0:
            for dvd in self.dvds:
                for trk in dvd.alltracks:
                    if trk.number in dvd.selected:
                        dvd.makeMp4(trk)
                os.rename(dvd.path, "{}/{}".format(self.processed, dvd.name))
