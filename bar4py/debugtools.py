import cv2

# Preview Functions

def drawCorners(points, frame):
    cv2.circle(frame, tuple(points[0]), 5, (0,0,255), 2)
    cv2.circle(frame, tuple(points[1]), 5, (0,255,0), 2)
    cv2.circle(frame, tuple(points[2]), 5, (0,255,255), 2)
    cv2.circle(frame, tuple(points[3]), 5, (255,0,0), 2)

def drawMarkersCorners(markers, frame):
    for marker in markers:
        points = marker.points
        cv2.circle(frame, tuple(points[0]), 5, (0,0,255), 2)
        cv2.circle(frame, tuple(points[1]), 5, (0,255,0), 2)
        cv2.circle(frame, tuple(points[2]), 5, (0,255,255), 2)
        cv2.circle(frame, tuple(points[3]), 5, (255,0,0), 2)

def drawMarkers(markers, frame):
    for marker in markers:
        points = marker.points
        cv2.circle(frame, tuple(points[0]), 5, (0,0,255), 2)
        cv2.circle(frame, tuple(points[1]), 5, (0,255,0), 2)
        cv2.circle(frame, tuple(points[2]), 5, (0,255,255), 2)
        cv2.circle(frame, tuple(points[3]), 5, (255,0,0), 2)

        center_pos = marker.calculateCenter()
        cv2.circle(frame, center_pos, 3, (0,0,255), 2)
        cv2.circle(frame, center_pos, 5, (0,255,0), 2)
        cv2.circle(frame, center_pos, 8, (255,0,0), 2)
        marker_id = marker.marker_id
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, str(marker_id), center_pos, font, 0.8, (0,0,255), 2, cv2.LINE_AA)
