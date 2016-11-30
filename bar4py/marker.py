import numpy as np

# Marker

class Marker:
    def __init__(self, corners=np.zeros((4,2), dtype='int32'),
                 mkid=0, rvec=None, tvec=None):
        self.corners = corners.reshape(4,2)
        self.mkid = mkid
        self.rvec = rvec 
        self.tvec = tvec
