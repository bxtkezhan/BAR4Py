import cv2
import numpy as np

# Marker

class Marker:
    def __init__(self, markerOBJ=None,
                 points=None, corners=None,
                 marker_id=None, rotations=None,
                 rvec=None, tvec=None):

        if markerOBJ is not None:
            self.points = markerOBJ.points
            self.corners = markerOBJ.corners
            self.marker_id = markerOBJ.marker_id
            self.rotations = markerOBJ.rotations
            self.rvec = markerOBJ.rvec 
            self.tvec = markerOBJ.tvec

        if points is not None:
            self.points = points
        else:
            self.corners = None
        if corners is not None:
            self.corners = corners.reshape(4,2)
        else:
            self.corners = None
        if marker_id is not None:
            self.marker_id = marker_id
        else:
            self.marker_id = -1
        if rotations is not None:
            self.rotations = rotations
        else:
            self.rotations = 0
        if rvec is not None:
            self.rvec = rvec 
        else:
            self.rvec = None
        if tvec is not None:
            self.tvec = tvec
        else:
            self.tvec = None


    def setPoints(self, points):
        return Marker(markerOBJ=self, points=points)

    def setCorners(self, corners):
        return Marker(markerOBJ=self, corners=corners)

    def setMarkerID(self, marker_id):
        return Marker(markerOBJ=self, marker_id=marker_id)

    def setRotations(self, rotations):
        return Marker(markerOBJ=self, rotations=rotations)

    def setRVEC(self, rvec):
        return Marker(markerOBJ=self, rvec=rvec)

    def setTVEC(self, tvec):
        return Marker(markerOBJ=self, tvec=tvec)

    def calculateExtrinsics(self, camera_matrix, dist_coeff):
        object_points = np.zeros((4,3), dtype=np.float32)
        object_points[:,:2] = np.mgrid[0:2,0:2].T.reshape(-1,2)
        marker_points = self.corners
        ret, rvec, tvec = cv2.solvePnP(object_points, marker_points,
                                       camera_matrix, dist_coeff)
        if ret: self.rvec, self.tvec = rvec, tvec
        return ret

    def calculateCenter(self, points=None):
        if points is None: points = self.points
        if points is None: raise TypeError('calculateCenter need a points value')

        '''
        Transform 1
        (y-y1)/(y2-y1)=(x-x1)/(x2-x1)
        => A: 1/(x2-x1), B: 1/(y1-y2)
        => C: - y1 * B - x1 * A
        => C: -(x1 * A + y1 * B)

        Transform 2
        A1x+B1y+C1=0, A2x+B2y+C2=0
        => x: (B1C2-B2C1)/(B2A1-B1A2), y: (A1C2-C1A2)/(B1A2-A1B2)
        '''
        l0_x0, l0_y0 = points[0]
        l0_x1, l0_y1 = points[2]
        l1_x0, l1_y0 = points[1]
        l1_x1, l1_y1 = points[3]

        A0 = 1/(l0_x1-l0_x0)
        B0 = 1/(l0_y0-l0_y1)
        C0 = -(l0_x0 * A0 + l0_y0 * B0)
        A1 = 1/(l1_x1-l1_x0)
        B1 = 1/(l1_y0-l1_y1)
        C1 = -(l1_x0 * A1 + l1_y0 * B1)

        x = (B0*C1-B1*C0)/(B1*A0-B0*A1)
        y = (A0*C1-C0*A1)/(B0*A1-A0*B1)

        return x.astype(int),y.astype(int)
