import cv2

from bar4py.shortfuncs import opjoin, filename2basename, bgr2gray
from glob import glob

class Dictionary:
    '''
    Dictionary Class, 2016/12/10 Edit

    Inputs:
    dictionaryObj is Dictionary object
    ids is marker_id list
    frames is marker frame list
    en_pool is contrl of set pool
    pool_size is default pool size

    For examples:
    >>> from bar4py.dictionary import Dictionary
    >>> dictionary = Dictionary()
    >>> dictionary = Dictionary(dictionary)
    >>> dictionary = Dictionary(dictionary, ids=ids, frames=frames)
    >>> dictionary = Dictionary(dictionary, en_pool, pool_size=(64,64))
    '''
    def __init__(self, dictionaryObj=None,
                 ids=None, frames=None,
                 en_pool=True, pool_size=(28, 28)):
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
        if not self.is_pooled and en_pool:
            self.frames = [self.poolFrame(frame, pool_size) for frame in self.frames]

    @property
    def is_pooled(self, dictionaryObj=None):
        dictionary = dictionaryObj or self
        if len(dictionary.frames) == 0:
            return False
        for frame in dictionary.frames:
            if len(frame.shape) != 2 or (frame.min(), frame.max()) != (0,1):
                return False
        return True

    def poolFrame(self, frame, pool_size=(28, 28)):
        '''
        frame is OpenCV image frame
        return pooled frame
        '''
        if len(frame.shape) == 2:
            gray_frame = frame
        else:
            gray_frame = bgr2gray(frame)
        pool_frame = cv2.resize(gray_frame, pool_size)
        _, pool_frame = cv2.threshold(pool_frame, pool_frame.mean(), 1, cv2.THRESH_OTSU)
        return pool_frame

    def buildByFilenames(self, filenames, ids=None, en_pool=True, pool_size=(28, 28)):
        '''
        filenames is image filenames
        Set self.frames by setFrames
        '''
        self.ids = ids or [filename2basename(filename) for filename in filenames]
        if en_pool:
            self.frames = [self.poolFrame(cv2.imread(filename), pool_size) for filename in filenames]
        else:
            self.frames = [cv2.imread(filename) for filename in filenames]

    def buildByDirectory(self, filetype, path='.', ids=None, en_pool=True, pool_size=(28, 28)):
        '''
        Set self.format by files in path and the file type is filetype
        '''
        filenames = glob(opjoin(path, filetype))
        self.buildByFilenames(filenames, ids, en_pool, pool_size)

    def append(self, marker_id=None, frame=None, en_pool=True, pool_size=(28, 28)):
        '''
        Append marker_id or frame to self
        '''
        marker_id and self.ids.append(marker_id)
        if frame is not None:
            if en_pool:
                frame = self.poolFrame(frame, pool_size)
            self.frames.append(frame)

    def setIDs(self, ids):
        '''
        Set ids and return new Dictionary object
        '''
        return Dictionary(self, ids=ids)

    def setFrames(self, frames, en_pool=True, pool_size=(28, 28)):
        '''
        Set frames and return new Dictionary object
        '''
        return Dictionary(self, frames=frames, en_pool=en_pool, pool_size=pool_size)

    def getDict(self, dictionaryObj=None):
        '''
        dictionaryObj is Dictionary object
        Return zip(ids, frames)
        '''
        dictionary = dictionaryObj or self
        min_size = min(len(dictionary.ids), len(dictionary.frames))
        return dict(zip(dictionary.ids[:min_size], dictionary.frames[:min_size]))

    def getPoolDict(self, dictionaryObj=None, pool_size=(28, 28)):
        '''
        dictionaryObj is Dictionary object
        Return pooled dictionary's zip(ids, frames)
        '''
        min_size = min(len(self.ids), len(self.frames))
        dictionary = dictionaryObj or self
        if dictionary.is_pooled: return dictionary.getDict()
        pool_frames = []
        for frame in dictionary.frames[:min_size]:
            pool_frame = self.poolFrame(frame, pool_size)
            pool_frames.append(pool_frame)
        return dict(zip(dictionary.ids[:min_size], pool_frames))

    @property
    def length(self):
        return len(self.ids)
