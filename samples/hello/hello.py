#! /usr/bin/env python3
import cv2
import numpy as np

from resconfig import *
from bar4py.debugtools import drawMarkers, drawAxis
from bar4py import CameraParameters, Dictionary, MarkerDetector

frame = cv2.imread(opjoin(RES_IMG, 'image-test.png'))

# Load Camera Parameters
cameraParameters = CameraParameters()
cameraParameters.readFromJsonFile(opjoin(RES_CAM, 'camera_640x480.json'))

# Create Dictionary
dictionary = Dictionary()
dictionary.buildByDirectory(filetype='*.jpg', path=RES_MRK)

# Create MarkerDetector
markerDetector = MarkerDetector(dictionary=dictionary, cameraParameters=cameraParameters)

# Detect
markers = markerDetector.detect(frame)

# Draw
drawMarkers(markers, frame)
drawAxis(cameraParameters, markers, frame)

# Show
cv2.imshow('Hello BAR4Py', frame)
cv2.waitKey(0) & 0xFF
cv2.destroyAllWindows()
