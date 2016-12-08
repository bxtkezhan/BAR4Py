import cv2
import numpy as np

# Marker

class Marker:
    '''
    Marker class, 2016/12/8 edit

    Inputs:
    markerOBJ is Marker opject
    Type of points is np.ndarray, and shape of points is (4,1,2) or (4,2) ...
    Type of marker_id is int, float, string ...

    For examples:
    >>> from bar4py.marker import Marker
    >>> marker = Marker()
    >>> marker = Marker(markerOBJ=marker)
    >>> marker = Marker(points=points)
    >>> marker = Marker(marker_id=marker_id)
    '''
    def __init__(self, markerOBJ=None, points=None, marker_id=None):
        # Default parameters
        self.points = None
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
        if marker_id is not None: self.marker_id = marker_id

    def setPoints(self, points):
        '''
        points type: ndarray, shape: (4,1,2) or (4,2) ...
        >>> marker_new = marker.setPoints(points)
        '''
        return Marker(markerOBJ=self, points=points)

    def setMarkerID(self, marker_id):
        '''
        marker_id type: int, float, string ...
        >>> marker_new = marker.setMarkerID(marker_id)
        '''
        return Marker(markerOBJ=self, marker_id=marker_id)

    def calculateCenter(self, points=None):
        '''
        points is Marker.points
        >>> x, y = marker.calculateCenter()
        '''
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

        T = 0.000001

        A0 = 1/(l0_x1-l0_x0+T)
        B0 = 1/(l0_y0-l0_y1+T)
        C0 = -(l0_x0 * A0 + l0_y0 * B0)
        A1 = 1/(l1_x1-l1_x0+T)
        B1 = 1/(l1_y0-l1_y1+T)
        C1 = -(l1_x0 * A1 + l1_y0 * B1)

        x = (B0*C1-B1*C0)/(B1*A0-B0*A1+T)
        y = (A0*C1-C0*A1)/(B0*A1-A0*B1+T)

        return x.astype(int),y.astype(int)

    def calculateCorners(self, gray, points=None):
        '''
        gray is OpenCV gray image,
        points is Marker.points
        >>> marker.calculateCorners(gray)
        >>> print(marker.corners)
        '''
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

    def calculateExtrinsics(self, camera_matrix, dist_coeff):
        '''
        Inputs:
        camera_matrix is OpenCV cameraMatrix
        dist_coeff is OpenCV distCoeff

        Return: rotate vector and transform vector

        >>> marker.calculateExtrinsics(camera_matrix, dist_coeff)
        >>> print(marker.rvec, marker.tvec)
        '''
        object_points = np.zeros((4,3), dtype=np.float32)
        object_points[:,:2] = np.mgrid[0:2,0:2].T.reshape(-1,2)
        marker_points = self.corners
        ret, rvec, tvec = cv2.solvePnP(object_points, marker_points,
                                       camera_matrix, dist_coeff)
        if ret: self.rvec, self.tvec = rvec, tvec
        return ret
