import cv2
import numpy as np

from resConfig import *
from ardebug import drawCorners, drawMarkersCorners
from shortfuncs import *

from marker import Marker
from markerDetector import MarkerDetector

# Debug Moduels.

def preview(imagefilename=None, videofilename='video.avi'):
    # Open capture
    if not imagefilename:
        cap = cv2.VideoCapture(opjoin(RES_VID, videofilename))

    # Create Dictionary
    dictionary = []
    for marker_id in [101]:
        hash_map = cv2.imread(opjoin(RES_MRK, '{}.jpg'.format(marker_id)))
        dictionary.append((marker_id, hash_map))
    # Create makerDetector and set dictionary
    markerDetector = MarkerDetector(dictionary=dictionary)
    while True:
        # Read video data
        if imagefilename:
            frame = cv2.imread(opjoin(RES_IMG, imagefilename))
        else:
            ret, frame = cap.read()
            if not ret: break

        markers, thresh = markerDetector.detect(frame, en_debug=True)
        drawMarkersCorners(markers, frame)
        cv2.imshow('TEST', frame)
        key = cv2.waitKey(100) & 0xFF
        if key == 27: break
        elif key == 32: cv2.waitKey(0)

    # Desctroy and release
    cv2.destroyAllWindows()
    if not imagefilename: cap.release()

if __name__ == '__main__':
    preview()
