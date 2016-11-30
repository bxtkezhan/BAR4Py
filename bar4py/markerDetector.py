import cv2
import numpy as np
from shortfuncs import *
from marker import Marker

# MarkerDetector

class MarkerDetector:
    def __init__(self, dictionary=None,
                 cameraMatrix=None, distCoeffs=None):
        self.dictionary = dictionary
        self.cameraMatrix = cameraMatrix
        self.distCoeffs = distCoeffs

    def isProbableMarker(self, approx_curve, limit=32):
        if approx_curve.shape != (4,1,2): return False
        if (min(np.sum((approx_curve[0] - approx_curve[2])**2),
                np.sum((approx_curve[1] - approx_curve[3])**2))
            >= limit**2): return True

    def localRect(self, corners):
        x0, y0 = corners[:,1].min(), corners[:,0].min()
        x1, y1 = corners[:,1].max(), corners[:,0].max()
        return np.array([x0, y0, x1, y1], dtype='uint32').reshape(2,2)

    def localFrame(self, rect, frame):
        return frame[rect[0,0]:rect[1,0], rect[0,1]:rect[1,1]]

    def localCorners(self, rect, corners):
        local_corners = np.zeros((4,2), dtype=corners.dtype)
        local_corners[:,0] = corners[:,0] - rect[0,1]
        local_corners[:,1] = corners[:,1] - rect[0,0]
        return local_corners

    def recognize(self, corners, frame, dictionary=None, limit=0.8, side_length=64):
        dictionary = dictionary or self.dictionary
        if dictionary is None: raise TypeError('recognize nead dictionary')

        corners_src = np.float32(corners)
        corners_dst = np.float32([[0,0],[0,side_length],[side_length,side_length],[side_length,0]])

        M = cv2.getPerspectiveTransform(corners_src, corners_dst)
        dst = cv2.warpPerspective(frame, M, (side_length, side_length))

        _, dst = cv2.threshold(dst, dst.mean(), 1, cv2.THRESH_OTSU)
        for marker_id, hash_map in dictionary:
            hash_map = cv2.resize(bgr2gray(hash_map), (side_length, side_length))
            _, hash_map = cv2.threshold(hash_map, hash_map.mean(), 1, cv2.THRESH_OTSU)
            for i in range(4):
                deviation = np.sum((dst == hash_map).astype(int)) / (side_length**2)
                if deviation > limit: return marker_id, i
                hash_map = np.rot90(hash_map, -1)


    def detect(self, frame, epsilon_rate=0.01, en_debug=False):
        # Output marker list
        markers = []

        if (not isinstance(frame, np.ndarray) and
            (len(frame.shape) < 2 or len(frame.shape) > 3)):
            TypeError('Input is not OpenCV image')

        # To Gray
        gray = frame
        if len(gray.shape) == 3: gray = bgr2gray(gray)

        # Thresh
        ret, thresh = cv2.threshold(gray, gray.mean(), 255,
                                    cv2.THRESH_BINARY)
        if not ret: return False

        # Find contours
        _, contours, _ = cv2.findContours(thresh, cv2.RETR_LIST,
                                          cv2.CHAIN_APPROX_NONE)

        # Probable Marker
        _markers = []
        for cnt in contours:
            epsilon = epsilon_rate * cv2.arcLength(cnt,True)
            approx_curve = cv2.approxPolyDP(cnt,epsilon,True)
            if self.isProbableMarker(approx_curve):
                _markers.append(Marker(approx_curve))

        # Matched Marker
        if self.dictionary:
            for marker in _markers:
                local_rect = self.localRect(marker.corners)
                local_gray = self.localFrame(local_rect, gray)
                local_corners = self.localCorners(local_rect, marker.corners)
                recognize_result = self.recognize(local_corners, local_gray)
                if recognize_result: markers.append(marker)
        else:
            markers = _markers

        if en_debug:
            return markers, thresh
        return markers
