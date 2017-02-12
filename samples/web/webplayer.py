#! /usr/bin/env python3
from resconfig import *
from bar4py import Dictionary, CameraParameters, createWebPlayer

# WebAR modules test.

# Build WebAPP arguments.
dictionary = Dictionary()
dictionary.buildByDirectory(filetype='*.jpg', path=opjoin(RES_MRK, 'mini'))
cameraParameters = CameraParameters()
cameraParameters.readFromJsonFile(opjoin(RES_CAM, 'camera_640x480.json'))

# Create WebAR player.
player = createWebPlayer(__name__, dictionary, cameraParameters,
                         player_rect=(0, 35, 640, 480)) # yapf: disable

# Set dictionary options
dictionary_opts = {
    '701': {
        'type': 'obj',
        'content': None,
        'mpath': '/static/model/',
        'mname': 'rocket.mtl',
        'opath': '/static/model/',
        'oname': 'rocket.obj',
        'visibleTag': 5
    }
}
player.setDictionaryOptions(dictionary_opts)

# Set models animate.
animate_js = '''
var RotateTag0 = 0;
var RotateTag1 = 0;
function animate(id, model) {
    if (id == '701') {
        model.rotateX(Math.PI/2);
        model.rotateY(RotateTag0);
        RotateTag0 += 0.1;
    } else if (id == '601') {
        model.translateZ(0.5);
        model.rotateX(RotateTag1);
        RotateTag1 += 0.1;
    }
}
'''
player.setAnimate(animate_js)

if __name__ == '__main__': player.run(port=8000, debug=True)
