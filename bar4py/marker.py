import cv2
import numpy as np

# Marker

class Marker:
    def __init__(self, markerOBJ=None,
                 points=None, corners=None,
                 marker_id=None, rotations=None,
                 rvec=None, tvec=None):
        # Default parameters
        self.corners = None
        self.corners = None
        self.marker_id = -1
        self.rotations = 0
        self.rvec = None
        self.tvec = None

        # If input marker object
        if markerOBJ is not None:
            self.points = markerOBJ.points
            self.corners = markerOBJ.corners
            self.marker_id = markerOBJ.marker_id
            self.rotations = markerOBJ.rotations
            self.rvec = markerOBJ.rvec 
            self.tvec = markerOBJ.tvec

        # Some parameters
        if points is not None: self.points = points.reshape(4,2)
        if corners is not None: self.corners = corners.reshape(4,2)
        if marker_id is not None: self.marker_id = marker_id
        if rotations is not None: self.rotations = rotations
        if rvec is not None: self.rvec = rvec 
        if tvec is not None: self.tvec = tvec

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

    def calculateCorners(self, gray, points=None):
        if points is None: points = self.points
        if points is None: raise TypeError('calculateCorners need a points value')
        '''
        rotations = 0 -> 0,1,2,3
        rotations = 1 -> 3,0,1,2
        rotations = 2 -> 2,3,0,1
        rotations = 3 -> 1,2,3,0
        => A: 1,0,3,2; B: 0,3,2,1; C: 2,1,0,3; D: 3,2,1,0
        '''
        i = self.rotations
        A = (1,0,3,2)[i]; B = (0,3,2,1)[i]; C = (2,1,0,3)[i]; D = (3,2,1,0)[i]
        corners = np.float32([points[A], points[B], points[C], points[D]])
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.1)
        self.corners = cv2.cornerSubPix(gray, corners, (5,5), (-1,-1), criteria)

    def calculateCenter(self, points=None):
        if points is None: points = self.points
        if points is None: raise TypeError('calculateCenter need a points value')
        '''
        Transform 1
        (y-y0)/(y1-y0)=(x-x0)/(x1-x0)
        => A: 1/(x1-x0), B: 1/(y0-y1)
        => C: - y0*B - x0*A
        => C: -(x0*A + y0*B)

        Transform 2
        A0*x+B0*y+C0=0, A1*x+B1*y+C1=0
        => x: (B0*C1-B1*C0)/(B1*A0-B0*A1)
        => y: (A0*C1-C0*A1)/(B0*A1-A0*B1)
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

    def calculateExtrinsics(self, camera_matrix, dist_coeff):
        object_points = np.zeros((4,3), dtype=np.float32)
        object_points[:,:2] = np.mgrid[0:2,0:2].T.reshape(-1,2)
        marker_points = self.corners
        ret, rvec, tvec = cv2.solvePnP(object_points, marker_points,
                                       camera_matrix, dist_coeff)
        if ret: self.rvec, self.tvec = rvec, tvec
        return ret
