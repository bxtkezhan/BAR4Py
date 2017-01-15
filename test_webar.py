from bar4py import createWebARApp

from resconfig import *
from bar4py import Dictionary, CameraParameters

dictionary = Dictionary()
dictionary.buildByDirectory(filetype='*.jpg', path=opjoin(RES_MRK, 'batchs'))
cameraParameters = CameraParameters()
cameraParameters.readFromJsonFile(opjoin(RES_CAM, 'camera_640x480.json'))

webAR = createWebARApp(dictionary, cameraParameters, (0, 35, 640, 480))
webAR.setDictionaryOptions({
    '701': {
        'type': 'obj',
        'content': None,
        'mpath': '/static/model/',
        'mname': 'mk.mtl',
        'opath': '/static/model/',
        'oname': 'mk.obj',
        'visibleTag': 5
    }
})

if __name__ == '__main__': webAR.run(port=8000, debug=True)
