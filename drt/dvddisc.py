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
class to manipulate dvd discs copied to a filesystem directory
"""

import os
from drt.dvdinfo import DVDInfo
from drt.dvdtrack import DVDChapter
from drt.dvdtrack import DVDTrack
import pickle
import logging

log = logging.getLogger(__name__)


class DVDDisc(object):
    def __init__(
        self,
        name,
        path,
        infodir,
        outputdir,
        handbrake,
        savedir,
        shortlen=300,
        preset="H.265 MKV 720p30",
    ):
        self.name = name
        self.startepisode = 1
        self.seriesid = 1
        self.seriesname = self.name
        self.path = path
        self.infodir = infodir
        self.outputdir = outputdir
        self.logdir = self.outputdir + "/logs"
        self.infofn = os.path.join(self.infodir, "{}.info".format(self.name))
        self.handbrake = handbrake
        self.savepath = savedir
        self.savefn = "{}/{}.saved".format(self.savepath, self.name)
        self.shortlen = shortlen
        self.preset = preset
        self.makeInfo()

    def saveMe(self):
        try:
            with open(self.savefn, "wb") as sfn:
                pickle.dump(self, sfn, pickle.HIGHEST_PROTOCOL)
            os.rename(self.path, "{}/{}".format(self.savepath, self.name))
        except Exception as e:
            msg = "oops, something went wrong saving: {}".format(e)

    def askMe(self, q, default):
        ret = default
        val = input("{} ({}) > ".format(q, default))
        if len(val) > 0:
            ret = val
        return ret

    def editMe(self):
        self.seriesname = self.askMe("Series Name", self.name)
        self.seriesid = int(self.askMe("Series number", 1))
        startepisode = self.askMe("Starting Episode Number", 1)
        self.setStartingEpisodeNumber(startepisode)

    def edittracks(self):
        self.showTracks()
        val = self.askMe(
            "edit (s)elected tracks, edit (b)urnin subtitles, edit track (n)ames", ""
        )
        if len(val) > 0:
            if val == "s":
                self.editSelected()
            elif val == "b":
                self.editBurnin()
            elif val == "n":
                self.trackNames()

    def showMe(self):
        op = "DVD: {}".format(self.name)
        op += "\nSeries Name: {}".format(self.seriesname)
        op += "\nSeries ID: {}".format(self.seriesid)
        op += "\nStart Episode: {}".format(self.startepisode)
        print(op)

    def showTracks(self):
        for trk in self.alltracks:
            op = "  + " if trk.number in self.selected else "    "
            op += "b " if trk.burnin else "  "
            op += "{} - {}".format(trk.number, trk.fname)
            op += " - {} - {}".format(trk.duration, trk.dursecs)
            op += " - {}/{}".format(trk.alang, trk.slang)
            if len(trk.title):
                op += " {}".format(trk.title)
            print(op)

    def getTrack(self, trknum):
        ret = None
        for trk in self.alltracks:
            if trk.number == trknum:
                ret = trk
                break
        return ret

    def editSelected(self):
        trks = self.askMe("Tracks to process", self.selected)
        if trks != self.selected:
            self.selected = self.makeTrackList(trks)
            self.currentepisode = self.startepisode
            self.renameTracks()

    def makeTrackList(self, tracks):
        if "," in tracks:
            ltrks = tracks.split(",")
        else:
            ltrks = tracks.split(" ")
        trks = []
        for trk in ltrks:
            trks.append(int(trk))
        return trks

    def editBurnin(self):
        self.showTracks()
        val = self.askMe("Toggle Burnin (Track Num or (A)ll)", "")
        if len(val) > 0:
            if val == "A":
                for tn in self.selected:
                    trk = self.getTrack(tn)
                    trk.toggleBurnin()
            else:
                try:
                    tn = int(val)
                    trk = self.getTrack(tn)
                    trk.toggleBurnin()
                except ValueError as e:
                    print("it's simple, enter a track NUMBER or 'A'")

    def trackNames(self):
        exitfunc = False
        while not exitfunc:
            self.showTracks()
            val = self.askMe("Select track number or (e)xit track editor.", "")
            if val != "e":
                try:
                    tn = int(val)
                    val = self.askMe("Track {} title:".format(tn), "")
                    if len(val) > 0:
                        trk = self.getTrack(tn)
                        trk.title = val
                except ValueError as e:
                    print(
                        "golly, please at least TRY to read the prompt, enter a NUMBER or 'e'"
                    )
            else:
                exitfunc = True

    def makeInfo(self):
        print("making info")
        cmd = "{} -i {} -t 0 >{} 2>&1".format(self.handbrake, self.path, self.infofn)
        print("cmd: {}".format(cmd))
        os.system(cmd)
        self.alltracks = []
        xinfo = DVDInfo(self.infofn, shortlen=self.shortlen)
        for track in xinfo.alltracks:
            trk = DVDTrack(track)
            trk.alang, trk.slang, trk.burnin = self.checkLang(trk)
            trk.fname = self.name + " {}".format(trk.episodenum)
            self.alltracks.append(trk)
        self.selected = xinfo.selected

    def checkLang(self, track):
        burnin = False
        alang = "none"
        slang = "none"
        an = len(track.audios)
        sn = len(track.subts)
        if an > 0 and sn > 0:
            alang = track.audios[0].lang
            slang = track.subts[0].lang
            if alang != slang:
                burnin = True
        return [alang, slang, burnin]

    def getSeriesTag(self):
        if self.seriesid == -1:
            return self.seriesname
        else:
            return (
                "{} S0{}".format(self.seriesname, self.seriesid)
                if self.seriesid < 10
                else "{} S{}".format(self.seriesname, self.seriesid)
            )

    def setStartingEpisodeNumber(self, episodenum):
        self.startepisode = int(episodenum)
        self.currentepisode = int(episodenum)
        self.renameTracks()

    def renameTracks(self):
        stag = self.getSeriesTag()
        for track in self.alltracks:
            if track.number in self.selected:
                if self.seriesid == -1:
                    track.fname = stag
                else:
                    track.setEpisodeNumber(self.currentepisode)
                    track.fname = "{}{}".format(stag, track.fname)
                self.currentepisode += 1
            else:
                track.fname = "{} {}".format(self.name, track.number)

    def makeMp4(self, track):
        # preset = "Fire TV 1080p30 Surround"
        # preset = "Fast 1080p30"
        try:
            preset = self.preset
        except AttributeError:
            preset = "H.265 MKV 720p30"
        burninopts = "--subtitle-lang-list eng --all-subtitles"
        cmd = "{} -i {} -t {} -Z '{}' ".format(
            self.handbrake, self.path, track.number, preset
        )
        if track.burnin:
            cmd += "{} ".format(burninopts)
        fname = "{}/{}".format(self.outputdir, track.fname)
        tname = track.fname
        if len(track.title):
            tname = "{} {}".format(track.fname, track.title)
            fname += " {}".format(track.title)
        fname += ".m4v"
        cmd += '-o "{}"'.format(fname)
        logfile = self.logdir + "/{}.handbrake.log".format(tname)
        cmd += ' >"{}" 2>&1'.format(logfile)
        print("processing track {}".format(track.number))
        print("cmd: {}".format(cmd))
        os.system(cmd)
        print("processing of track {} completed.".format(track.number))
