import cv2
import numpy as np

from resconfig import *
from bar4py.debugtools import drawAxis, drawMarkers
from bar4py import CameraParameters, Dictionary, MarkerDetector

# Dump Datas Moduel.

def dumpDatas(imagefilename=None, videofilename='video.avi'):
    # Open capture
    if not imagefilename:
        cap = cv2.VideoCapture(opjoin(RES_VID, videofilename))

    # Load Camera Parameters
    cameraParameters = CameraParameters()
    cameraParameters.readFromJsonFile(opjoin(RES_CAM, 'camera_640x480.json'))
    print('GLPV:', cameraParameters.cvt2GLProjection(640, 480).tolist())
    import os
    if not os.path.isdir('test-matrix'): os.mkdir('test-matrix')
    np.savetxt('test-matrix/cam.txt', cameraParameters.cvt2GLProjection(640, 480).reshape(1,16), delimiter=',')
    # Create Dictionary
    dictionary = Dictionary()
    dictionary.buildByDirectory(filetype='*.jpg', path=RES_MRK)
    # Create MarkerDetector
    markerDetector = MarkerDetector(dictionary=dictionary, cameraParameters=cameraParameters)
    # Read video data
    if imagefilename:
        frame = cv2.imread(opjoin(RES_IMG, imagefilename))
    else:
        ret, frame = cap.read()
        if ret: cap.release() 
        else: return False
    markers = markerDetector.detect(frame)
    for marker in markers:
        print('ID:', marker.marker_id)
        print('RVEC:')
        print(marker.rvec)
        print('TVEC:')
        print(marker.tvec)
        print('GLMV:')
        print(marker.cvt2TJModelView())
        print('-'*32)
        np.savetxt('test-matrix/mk_{}.txt'.format(marker.marker_id), marker.cvt2GLModelView().reshape(1,16), delimiter=',')
    drawAxis(cameraParameters, markers, frame)
    drawMarkers(markers, frame)
    cv2.imwrite('test-image.jpg', frame)

if __name__ == '__main__': dumpDatas()
