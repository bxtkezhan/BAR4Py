import cv2

from shortfuncs import *

class Dictionary:
    def __init__(self, dictionaryObj=None,
                 ids=None, frames=None):
        self.ids = []
        self.frames = []
        if dictionaryObj is not None:
            self.ids = dictionaryObj.ids
            self.frames = dictionaryObj.frames
        if ids is not None:
            self.ids = ids
        if frames is not None:
            self.frames = frames

    def setIDs(self, ids):
        if len(ids) != len(self.frames):
            raise TypeError('Input ids size != self.frames size')
        return Dictionary(self, ids=ids)

    def setFrames(self, frames):
        if len(self.ids) != len(frames):
            raise TypeError('Input frames size != self.ids size')
        return Dictionary(self, frames=frames)

    def getDict(self):
        return zip(self.ids, self.frames)

    def getPoolDict(self, size, dictionaryObj=None):
        dictionary = dictionaryObj or self
        pool_frames = []
        for frame in dictionary.frames:
            pool_frame = cv2.resize(bgr2gray(frame), size)
            _, pool_frame = cv2.threshold(pool_frame, pool_frame.mean(), 1, cv2.THRESH_OTSU)
            pool_frames.append(pool_frame)
        return zip(dictionary.ids, pool_frames)
