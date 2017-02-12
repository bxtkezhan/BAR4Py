import cv2
import numpy as np

# Preview Functions

def drawCorners(points, frame):
    cv2.circle(frame, tuple(points[0]), 5, (0,0,255), 2)
    cv2.circle(frame, tuple(points[1]), 5, (0,255,0), 2)
    cv2.circle(frame, tuple(points[2]), 5, (0,255,255), 2)
    cv2.circle(frame, tuple(points[3]), 5, (255,0,0), 2)

def drawMarkersCorners(markers, frame):
    for marker in markers:
        points = marker.points
        drawCorners(points, frame)

def drawMarkers(markers, frame):
    for marker in markers:
        drawCorners(marker.points, frame)

        center = marker.calculateCenter()
        cv2.circle(frame, center, 3, (0,0,255), 2)
        cv2.circle(frame, center, 5, (0,255,0), 2)
        cv2.circle(frame, center, 8, (255,0,0), 2)
        marker_id = marker.marker_id
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, str(marker_id), center, font, 0.8, (0,0,255), 2, cv2.LINE_AA)

def drawMarkersArea(area, frame):
    l, t, r, b = area
    cv2.rectangle(frame, (l, t), (r, b), (255, 64, 128), 2)

def drawAxis(camera_parameters, markers, frame):
    axis = np.float32([[1,0,0], [0,1,0], [0,0,1]]).reshape(-1,3)
    mtx, dist = camera_parameters.camera_matrix, camera_parameters.dist_coeff

    for marker in markers:
        rvec, tvec = marker.rvec, marker.tvec
        imgpts, jac = cv2.projectPoints(axis, rvec, tvec, mtx, dist)
        corners = marker.corners
        corner = tuple(corners[0].ravel())
        cv2.line(frame, corner, tuple(imgpts[0].ravel()), (0,0,255), 2)
        cv2.line(frame, corner, tuple(imgpts[1].ravel()), (0,255,0), 2)
        cv2.line(frame, corner, tuple(imgpts[2].ravel()), (255,0,0), 2)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, 'X', tuple(imgpts[0].ravel()), font, 0.5, (0,0,255), 2, cv2.LINE_AA)
        cv2.putText(frame, 'Y', tuple(imgpts[1].ravel()), font, 0.5, (0,255,0), 2, cv2.LINE_AA)
        cv2.putText(frame, 'Z', tuple(imgpts[2].ravel()), font, 0.5, (255,0,0), 2, cv2.LINE_AA)

def drawBox(camera_parameters, markers, frame):
    objpts = np.float32([[0,0,0], [1,0,0], [1,1,0], [0,1,0],
                         [0,0,1], [1,0,1], [1,1,1], [0,1,1]]).reshape(-1,3)
    mtx, dist = camera_parameters.camera_matrix, camera_parameters.dist_coeff

    for marker in markers:
        rvec, tvec = marker.rvec, marker.tvec
        imgpts, jac = cv2.projectPoints(objpts, rvec, tvec, mtx, dist)

        cv2.line(frame, tuple(imgpts[0].ravel()), tuple(imgpts[1].ravel()), (0,0,255), 2)
        cv2.line(frame, tuple(imgpts[1].ravel()), tuple(imgpts[2].ravel()), (0,0,255), 2)
        cv2.line(frame, tuple(imgpts[2].ravel()), tuple(imgpts[3].ravel()), (0,0,255), 2)
        cv2.line(frame, tuple(imgpts[3].ravel()), tuple(imgpts[0].ravel()), (0,0,255), 2)

        cv2.line(frame, tuple(imgpts[0].ravel()), tuple(imgpts[0+4].ravel()), (0,0,255), 2)
        cv2.line(frame, tuple(imgpts[1].ravel()), tuple(imgpts[1+4].ravel()), (0,0,255), 2)
        cv2.line(frame, tuple(imgpts[2].ravel()), tuple(imgpts[2+4].ravel()), (0,0,255), 2)
        cv2.line(frame, tuple(imgpts[3].ravel()), tuple(imgpts[3+4].ravel()), (0,0,255), 2)

        cv2.line(frame, tuple(imgpts[0+4].ravel()), tuple(imgpts[1+4].ravel()), (0,0,255), 2)
        cv2.line(frame, tuple(imgpts[1+4].ravel()), tuple(imgpts[2+4].ravel()), (0,0,255), 2)
        cv2.line(frame, tuple(imgpts[2+4].ravel()), tuple(imgpts[3+4].ravel()), (0,0,255), 2)
        cv2.line(frame, tuple(imgpts[3+4].ravel()), tuple(imgpts[0+4].ravel()), (0,0,255), 2)
