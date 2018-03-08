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
class to generate information about a DVD from a HandBrake .info file
"""

import re
from drt.filesystem import FileSystem
from drt.filesystem import FileNotFound

class DVDInfo(object):
    def __init__(self, path, shortlen=300):
        self.dre = re.compile(r'duration:? (\d{2}:\d{2}:\d{2})')
        self.cre = re.compile(r'\+ (\d+): cells.*, (\d+).*, duration (\d{2}:\d{2}:\d{2})')
        self.are = re.compile(r'\+ (\d+), (\w+) .*')
        self.sre = re.compile(r'\+ (\d+), (\w+) .*')
        self.shortlen = shortlen
        fs = FileSystem()
        if not fs.fileExists(path):
            raise(FileNotFound(path))
        blocks = self.readInfo(path)
        self.alltracks = []
        for block in blocks:
            track = self.processTrack(block["block"])
            self.alltracks.append({"tracknum": block["tracknum"], "data":track})
        tracks = self.removeShorts()
        tracks = self.doDuplicates(tracks)
        self.selected = []
        for track in tracks:
            self.selected.append(int(track["tracknum"]))

    def doDuplicates(self, tracks):
        duplicate = True
        while duplicate:
            duplicate = False
            for track in tracks:
                xtrack = self.findDuplicateTracks(track, tracks)
                if xtrack is not None:
                    duplicate = True
                    tracks = self.popTrackNum(xtrack["tracknum"], tracks)
                    break
        return tracks

    def readInfo(self, path):
        tre = re.compile(r'\d+')
        blocks = []
        firstline = False
        inblock = False
        mf = "  + Main Feature"
        tracknum = 0
        with open(path, "r") as fn:
            content = fn.readlines()
        for line in content:
            if line.startswith("+ title"):
                if inblock:
                    track = {"tracknum": tracknum, "block": block}
                    blocks.append(track)
                else:
                    inblock = True
                block = []
                firstline = True
            if inblock:
                if not firstline:
                    if not line.startswith(mf):
                        block.append(line.strip())
                else:
                    firstline = False
                    m = tre.search(line)
                    if m:
                        tracknum = m.group()
        track = {"tracknum": tracknum, "block": block}
        blocks.append(track)
        return blocks

    def popTrackNum(self, xtrknum, tracks):
        cn = len(tracks)
        for x in range(0, cn):
            if tracks[x]["tracknum"] == xtrknum:
                # print("removing track {}".format(xtrknum))
                tracks.pop(x)
                break
        return tracks

    def findDuplicateTracks(self, track, tracks):
        ret = None
        for xtrack in tracks:
            if track["tracknum"] != xtrack["tracknum"]:
                if self.compareTracks(track["data"], xtrack["data"]):
                    ret = xtrack
                    break
        return ret

    def removeShorts(self):
        xos=[]
        for track in self.alltracks:
            if track["data"]["dursecs"] >= self.shortlen:
                xos.append(track)
        return xos

    def secs(self, xhms):
        hours, mins, secs = xhms.split(":")
        s = int(hours) * 3600
        s += (int(mins) * 60)
        s += int(secs)
        return s

    def grabDuration(self, dur):
        m=self.dre.search(dur)
        return m.group(1)

    def processChapter(self, c):
        ret = None
        m = self.cre.search(c)
        if m is not None:
            cnum = m.group(1)
            blocks = m.group(2)
            duration = m.group(3)
            dursecs = self.secs(duration)
            ret = [cnum, blocks, duration, dursecs]
        return ret

    def processAudio(self, al):
        ret = None
        m = self.are.search(al)
        if m is not None:
            anum = m.group(1)
            lang = m.group(2)
            ret = [anum, lang]
        return ret

    def processSubT(self, sl):
        ret = None
        m = self.sre.search(sl)
        if m is not None:
            snum = m.group(1)
            lang = m.group(2)
            ret = [snum, lang]
        return ret

    def processTrack(self, bl):
        chapters = []
        audios = []
        subts = []
        duration = 0
        dursecs = 0
        inchap = inaudio = insubt = False
        for line in bl:
            if line.startswith("+ duration"):
                duration = self.grabDuration(line)
                dursecs = self.secs(duration)
            elif line.startswith("+ chapters"):
                inchap = True
                inaudio = insubt = False
                continue
            elif line.startswith("+ audio"):
                inaudio = True
                inchap = insubt = False
                continue
            elif line.startswith("+ subtitle"):
                insubt = True
                inchap = inaudio = False
                continue
            elif inchap:
                chap = self.processChapter(line)
                if chap is not None:
                    chapter = { "cnum": chap[0], "blocks": chap[1],
                            "duration": chap[2], "dursecs": chap[3]}
                    chapters.append(chapter)
            elif inaudio:
                atest = self.processAudio(line)
                if atest is not None:
                    audio = {"anum": atest[0], "lang": atest[1]}
                    audios.append(audio)
            elif insubt:
                # print("in subtitle: {}".format(line))
                stest = self.processSubT(line)
                if stest is not None:
                    # print("adding subtitle")
                    subt = {"snum": stest[0], "lang": stest[1]}
                    subts.append(subt)
        return {"duration": duration, "dursecs": dursecs, "chapters": chapters, "audios": audios, "subtitles": subts}

    def compareTracks(self, t1, t2):
        ret = False
        if t1["dursecs"] == t2["dursecs"]:
            cn1 = len(t1["chapters"])
            cn2 = len(t2["chapters"])
            if cn1 == cn2:
                for cn in range(0,cn1):
                    if t1["chapters"][cn]["blocks"] != t2["chapters"][cn]["blocks"]:
                        break
                if cn == cn1 -1:
                    ret = True
        return ret

