import cv2
import numpy as np
from shortfuncs import *
from marker import Marker

# MarkerDetector

class MarkerDetector:
    def __init__(self, markerDetectorOBJ=None,
                 dictionary=None, camera_matrix=None, dist_coeffs=None):
        # Default parameters
        self.dictionary = None
        self.camera_matrix = None
        self.dist_coeffs = None

        # If input makerDetector object
        if markerDetectorOBJ is not None:
            self.dictionary = markerDetectorOBJ.dictionary
            self.camera_matrix = markerDetectorOBJ.camera_matrix
            self.dist_coeffs = markerDetectorOBJ.dist_coeffs

        # Some parameters
        if dictionary is not None:
            self.dictionary = dictionary
        if camera_matrix is not None:
            self.camera_matrix = camera_matrix
        if dist_coeffs is not None:
            self.dist_coeffs = dist_coeffs

        if self.dictionary:
            if not self.dictionary.isPooled():
                raise TypeError('Please input pooled dictionary')

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

    def recognize(self, points, frame, dictionary=None, limit=0.8, side_length=42, batch_size=3):
        dictionary = dictionary or self.dictionary
        if dictionary is None: raise TypeError('recognize nead dictionary')

        # To Gray
        gray = frame
        if len(gray.shape) == 3: gray = bgr2gray(frame)

        # Convert the points, gray to local_points, local_gray
        rect = self.localRect(points)
        gray = self.localFrame(rect, gray)
        points = self.localCorners(rect, points)

        # Define src_points and dst_points, src: 0,1,2,3 -> dst: 1,0,3,2
        points_src = np.float32(points)
        points_dst = np.float32([[0,side_length],[0,0], 
                                 [side_length,0],[side_length,side_length]])
    

        # Calc transform matrix and perspective dst map
        M = cv2.getPerspectiveTransform(points_src, points_dst)
        dst = cv2.warpPerspective(gray, M, (side_length, side_length))

        # Begin recognize
        _, dst = cv2.threshold(dst, dst.mean(), 1, cv2.THRESH_OTSU)
        # Probables
        probables = []
        for marker_id, hash_map in dictionary.getDict():
            # hash_map = cv2.resize(bgr2gray(hash_map), (side_length, side_length))
            # _, hash_map = cv2.threshold(hash_map, hash_map.mean(), 1, cv2.THRESH_OTSU)
            deviation = rotations = 0
            for i in range(4):
                now_deviation = np.sum((dst == hash_map).astype(int)) / (side_length**2)
                if now_deviation > deviation: deviation, rotations = now_deviation, i
                hash_map = np.rot90(hash_map)
            if deviation > limit:
                probables.append((deviation, marker_id, rotations))
                if len(probables) > batch_size: break
        # Best of marker_id and rotations
        if len(probables) > 0:
            return max(probables, key=lambda item:item[0])[1:]

    def detect(self, frame, epsilon_rate=0.01, en_debug=False):
        # Output marker list
        markers = []

        # To Gray
        gray = frame
        if len(gray.shape) == 3: gray = bgr2gray(frame)

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
                points = approx_curve.reshape(4,2)
                _markers.append(Marker(points=points))

        # Matched Marker
        if self.dictionary:
            for marker in _markers:
                rst = self.recognize(marker.points, gray)
                if rst:
                    marker.marker_id, marker.rotations = rst
                    marker.calculateCorners(gray)
                    markers.append(marker)
        else:
            markers = _markers

        if en_debug:
            return markers, thresh
        return markers
