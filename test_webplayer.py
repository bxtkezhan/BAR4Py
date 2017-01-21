from resconfig import *
from bar4py import Dictionary, CameraParameters, createWebPlayer

dictionary = Dictionary()
dictionary.buildByDirectory(filetype='*.jpg', path=opjoin(RES_MRK, 'batchs'))
cameraParameters = CameraParameters()
cameraParameters.readFromJsonFile(opjoin(RES_CAM, 'camera_640x480.json'))

player = createWebPlayer(dictionary, cameraParameters, (0, 35, 640, 480))
player.setDictionaryOptions({
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

animate_js = '''
var RotateTag0 = 0;
var RotateTag1 = 0;
function animate(id, model) {
    if (id == '701') {
        model.rotateZ(RotateTag0);
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
