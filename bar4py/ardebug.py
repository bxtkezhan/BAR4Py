import cv2

# Preview Functions

def drawCorners(corners, frame):
    cv2.circle(frame, tuple(corners[0]), 5, (0,0,255), 2)
    cv2.circle(frame, tuple(corners[1]), 5, (0,255,0), 2)
    cv2.circle(frame, tuple(corners[2]), 5, (0,255,255), 2)
    cv2.circle(frame, tuple(corners[3]), 5, (255,0,0), 2)

def drawMarkersCorners(markers, frame):
    for marker in markers:
        corners = marker.corners
        cv2.circle(frame, tuple(corners[0]), 5, (0,0,255), 2)
        cv2.circle(frame, tuple(corners[1]), 5, (0,255,0), 2)
        cv2.circle(frame, tuple(corners[2]), 5, (0,255,255), 2)
        cv2.circle(frame, tuple(corners[3]), 5, (255,0,0), 2)
