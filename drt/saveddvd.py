"""
class for each saved dvd
"""

import os
import pickle
import logging

log = logging.getLogger(__name__)

class SavedDvd(object):
    def __init__(self, name, path, incomingdir, processeddir):
        self.dvd = None
        self.name = name
        self.path = path
        self.incomingdir = incomingdir
        self.processeddir = processeddir
        self.pickled = "{}.saved".format(self.path)
        if os.path.isfile(self.pickled) and os.path.isdir(self.path):
            self.unPickle()

    def unPickle(self):
        with open(self.pickled, "rb") as sfn:
            self.dvd = pickle.load(sfn)

    def moveToIncoming(self):
        os.rename(self.path, "{}/{}".format(self.incomingdir, self.name))
        os.rename(self.pickled, "{}/{}".format(self.processeddir, os.path.basename(self.pickled)))

    def unMoveToIncoming(self):
        os.rename("{}/{}".format(self.incomingdir, self.name), self.path)
        os.rename("{}/{}".format(self.processeddir, os.path.basename(self.pickled)), self.pickled)
