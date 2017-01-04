import cv2
import numpy as np

from resconfig import *
from bar4py import webAR
from bar4py.debugtools import drawAxis, drawMarkers
from bar4py import CameraParameters, Dictionary, MarkerDetector

# Load Camera Parameters
cameraParameters = CameraParameters()
cameraParameters.readFromJsonFile(opjoin(RES_CAM, 'camera_640x480.json'))
dictionary = Dictionary()
dictionary.buildByDirectory(filetype='*.jpg', path=RES_MRK)
markerDetector = MarkerDetector(dictionary=dictionary, cameraParameters=cameraParameters)

webAR.markerDetector = markerDetector

if __name__ == '__main__': webAR.run(port=8000, debug=True)
