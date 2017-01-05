from bar4py.web import createWebARApp

from resconfig import *
from bar4py import Dictionary, CameraParameters

dictionary = Dictionary()
dictionary.buildByDirectory(filetype='*.jpg', path=RES_MRK)
cameraParameters = CameraParameters()
cameraParameters.readFromJsonFile(opjoin(RES_CAM, 'camera_640x480.json'))

webAR = createWebARApp(dictionary, cameraParameters, camera_size=(640, 480), video_rect=(0, 50, 640, 480))

if __name__ == '__main__': webAR.run(port=8000, debug=False)
