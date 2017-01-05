from flask import Flask, render_template, request, jsonify
import base64
import numpy as np
import cv2

from bar4py import Dictionary, CameraParameters, MarkerDetector

def cvt2TJDictionary(dictionary):
    tj_dictionary = {marker_id: {'type': 'cube', 'content': None, 'visibleTag': 5}
                     for marker_id in dictionary.ids}
    return tj_dictionary

def cvt2TJProjection(cameraParameters, size):
    P = cameraParameters.cvt2Projection(size[0], size[1])
    return P.flatten().tolist()

def cvt2TJModelView(marker, Rx=np.array([[1,0,0],[0,-1,0],[0,0,-1]])):
    M = marker.cvt2ModelView(Rx)
    return M.flatten().tolist()

def initArgs(video_rect, debug=False):
    return dict(
        left = video_rect[0],
        top = video_rect[1],
        width = video_rect[2],
        height = video_rect[3],
        debug = debug,
    )

def createWebARApp(dictionary, cameraParameters, camera_size, video_rect):
    app = Flask(__name__)

    if dictionary is not None:
        app.dictionary = cvt2TJDictionary(dictionary)

    if (cameraParameters is not None) and (camera_size is not None):
        app.projection = cvt2TJProjection(cameraParameters, camera_size)

    if (dictionary is not None) and (cameraParameters is not None):
        app.markerDetector = MarkerDetector(dictionary=dictionary, cameraParameters=cameraParameters)

    app.args = initArgs(video_rect, debug=app.config['DEBUG'])
    app.args['dictionary'] = app.dictionary
    app.args['projection'] = app.projection

    # Load cameraParameters and dictionary and set markerDetector.
    @app.route('/')
    def index():
        if app.config['DEBUG']: js_tag = np.random.randint(0, 1000000)
        else: js_tag = 'webAR'
        return render_template('index.tpl', js_tag=js_tag, args=app.args)

    @app.route('/initapp')
    def initApp():
        return jsonify(app.args)

    @app.route('/loaddictionary')
    def loadDictionary():
        return jsonify(app.dictionary)

    @app.route('/loadprojection')
    def loadProjection():
        return jsonify(app.projection)

    # Load b64Frame and find markers matrix.
    @app.route('/loadmodelviews', methods=['POST'])
    def loadModelViews():
        if request.form['b64Frame'] is None: return 'fails'
        b64 = request.form['b64Frame'].encode()
        cvt = base64.b64decode(b64)
        arr = np.frombuffer(base64.b64decode(cvt[22:]), np.uint8)
        frame = cv2.resize(cv2.imdecode(arr, 0), (app.args['width'], app.args['height']))
        markers = app.markerDetector.detect(frame)
        modelview_dict = {}
        for marker in markers:
            modelview_dict[marker.marker_id] = cvt2TJModelView(marker)
        return jsonify(modelview_dict)

    # TEST.
    @app.route('/test')
    def test(): return jsonify(app.dictionary)

    return app
