import cv2
import numpy as np

from resconfig import *
from shortfuncs import *
from debugtools import *

from dictionary import Dictionary
from markerdetector import MarkerDetector
from cameraparameters import CameraParameters

# Preview Moduels.

def preview(imagefilename=None, videofilename='video.avi'):
    # Open capture
    if not imagefilename:
        cap = cv2.VideoCapture(opjoin(RES_VID, videofilename))

    # Load Camera Parameters
    cameraParameters = CameraParameters()
    cameraParameters.readFromJsonFile(opjoin(RES_CAM, 'camera0.json'))
    # Create Dictionary
    dictionary = Dictionary()
    dictionary.buildByDirectory(filetype='*.jpg', path=RES_MRK)
    # Create MarkerDetector
    markerDetector = MarkerDetector(dictionary=dictionary)
    while True:
        # Read video data
        if imagefilename:
            frame = cv2.imread(opjoin(RES_IMG, imagefilename))
        else:
            ret, frame = cap.read()
            if not ret: break
        markers = markerDetector.detect(frame)
        for marker in markers:
            marker.calculateExtrinsics(cameraParameters.camera_matrix, cameraParameters.dist_coeff)
            print('ID:', marker.marker_id)
            print('RVEC:')
            print(marker.rvec)
            print('TVEC:')
            print(marker.tvec)
            print('-'*32)
        drawAxis(cameraParameters, markers, frame)
        drawMarkers(markers, frame)
        cv2.imshow('TEST', frame)
        key = cv2.waitKey(100) & 0xFF
        if key == 27: break
        elif key == 32: cv2.waitKey(0)

    # Desctroy and release
    cv2.destroyAllWindows()
    if not imagefilename: cap.release()

if __name__ == '__main__':
    preview()
