import cv2

from bar4py.shortfuncs import *
from os.path import join as opjoin
from os.path import basename
from glob import glob

class Dictionary:
    def __init__(self, dictionaryObj=None,
                 ids=None, frames=None,
                 en_pool=True, pool_size=(42,42)):
        # Default parameters
        self.ids = []
        self.frames = []

        # If dictionary object is not None
        if dictionaryObj is not None:
            self.ids = dictionaryObj.ids
            self.frames = dictionaryObj.frames
        if ids is not None:
            self.ids = ids
        if frames is not None:
            self.frames = frames

        # To pool
        if not self.isPooled() and en_pool:
            self.frames = [self.poolFrame(frame, pool_size) for frame in self.frames]

    def isPooled(self, dictionaryObj=None):
        dictionary = dictionaryObj or self
        if len(dictionary.frames) == 0:
            return False
        for frame in dictionary.frames:
            if len(frame.shape) != 2 or (frame.min(), frame.max()) != (0,1):
                return False
        return True

    def poolFrame(self, frame, pool_size=(42,42)):
            pool_frame = cv2.resize(bgr2gray(frame), pool_size)
            _, pool_frame = cv2.threshold(pool_frame, pool_frame.mean(), 1, cv2.THRESH_OTSU)
            return pool_frame

    def buildByFilenames(self, filenames, ids=None, en_pool=True, pool_size=(42,42)):
        self.ids = ids or [basename(filename).split('.')[0] for filename in filenames]
        if en_pool:
            self.frames = [self.poolFrame(cv2.imread(filename), pool_size) for filename in filenames]
        else:
            self.frames = [cv2.imread(filename) for filename in filenames]

    def buildByDirectory(self, filetype, path='.', ids=None, en_pool=True, pool_size=(42,42)):
        filenames = glob(opjoin(path, filetype))
        self.buildByFilenames(filenames, ids, en_pool, pool_size)

    def append(self, marker_id=None, frame=None, en_pool=True, pool_size=(42,42)):
        marker_id and self.ids.append(marker_id)
        if frame is not None:
            if en_pool:
                frame = self.poolFrame(frame, pool_size)
            self.frames.append(frame)

    def setIDs(self, ids):
        return Dictionary(self, ids=ids)

    def setFrames(self, frames, en_pool=True, pool_size=(42,42)):
        return Dictionary(self, frames=frames, en_pool=en_pool, pool_size=pool_size)

    def getDict(self, dictionaryObj=None):
        dictionary = dictionaryObj or self
        min_size = min(len(dictionary.ids), len(dictionary.frames))
        return zip(dictionary.ids[:min_size], dictionary.frames[:min_size])

    def getPoolDict(self, dictionaryObj=None, pool_size=(42,42)):
        min_size = min(len(self.ids), len(self.frames))
        dictionary = dictionaryObj or self
        if dictionary.isPooled(): return dictionary.getDict()
        pool_frames = []
        for frame in dictionary.frames[:min_size]:
            pool_frame = self.poolFrame(frame, pool_size)
            pool_frames.append(pool_frame)
        return zip(dictionary.ids[:min_size], pool_frames)
