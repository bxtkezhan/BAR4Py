import numpy as np

# Marker

class Marker:
    def __init__(self, corners=np.zeros((4,2), dtype='int32'),
                 marker_id=-1, rvec=None, tvec=None):
        self.corners = corners.reshape(4,2)
        self.marker_id = marker_id
        self.rvec = rvec 
        self.tvec = tvec
