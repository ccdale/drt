"""
class for each track on a DVD
"""
import logging

log = logging.getLogger(__name__)

class DVDTrack(object):
    def __init__(self,track):
        self.number = int(track["tracknum"])
        self.episodenum = self.number
        self.name = "{}".format(self.number)
        self.fname = "{}".format(self.episodenum)
        self.title = ""
        self.duration = track["data"]["duration"]
        self.dursecs = track["data"]["dursecs"]
        self.chapters = []
        self.audios = []
        self.subts = []
        self.burnin = False
        self.alang = "none"
        self.slang = "none"
        for chapter in track["data"]["chapters"]:
            dchap = DVDChapter(chapter)
            self.chapters.append(dchap)
        self.numchapters = len(self.chapters)
        for audio in track["data"]["audios"]:
            daudio = DVDAudio(audio)
            self.audios.append(daudio)
        for subt in track["data"]["subtitles"]:
            dsubt = DVDSubtitle(subt)
            self.subts.append(dsubt)

    def __str__(self):
        return "{}: {} ({}s)".format(self.number, self.duration, self.dursecs)

    def setBurnin(self, burnin, alang="none", slang="none"):
        self.burnin = burnin
        self.alang = alang
        self.slang = slang

    def toggleBurnin(self):
        self.burnin = not self.burnin

    def setEpisodeNumber(self, episodenum):
        self.episodenum = int(episodenum)
        self.fname = self.getEpisodeTag()

    def getEpisodeTag(self):
        return "E0{}".format(self.episodenum) if self.episodenum < 10 else "E{}".format(self.episodenum)

class DVDChapter(object):
    def __init__(self, chapter):
        self.number = chapter["cnum"]
        self.blocks = chapter["blocks"]
        self.duration = chapter["duration"]
        self.dursecs = chapter["dursecs"]

    def __str__(self):
        return "{}: {} ({}s)".format(self.number, self.duration, self.dursecs)

class DVDAudio(object):
    def __init__(self, audio):
        self.number = audio["anum"]
        self.lang = audio["lang"]

    def __str__(self):
        return "{} {}".format(self.number, self.lang)

class DVDSubtitle(object):
    def __init__(self, subt):
        self.number = subt["snum"]
        self.lang = subt["lang"]

    def __str__(self):
        return "{} {}".format(self.number, self.lang)
