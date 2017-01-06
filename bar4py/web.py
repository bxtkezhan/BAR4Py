from flask import Flask, render_template, request, jsonify
import base64
import numpy as np
import cv2

from bar4py import Dictionary, CameraParameters, MarkerDetector

def cvt2TJDictionary(dictionary):
    tj_dictionary = {marker_id: {'type': 'cube', 'content': None, 'visibleTag': 3}
                     for marker_id in dictionary.ids}
    return tj_dictionary

def cvt2TJProjection(cameraParameters):
    P = cameraParameters.cvt2Projection()
    return P.flatten().tolist()

def cvt2TJModelView(marker, Rx=np.array([[1,0,0],[0,-1,0],[0,0,-1]])):
    M = marker.cvt2ModelView(Rx)
    return M.flatten().tolist()

def initArgs(app, **args):
    if not hasattr(app, 'args'): app.args = {}
    app.args['DICTIONARY'] = app.dictionary
    app.args['PROJECTION'] = app.projection
    app.args['DEBUG'] = app.config['DEBUG']
    app.args['PLAYER_RECT'] = (0, 35, 640, 480)
    app.args.update(args)

def createWebARApp(dictionary, cameraParameters, player_rect):
    app = Flask(__name__)

    app.dictionary = cvt2TJDictionary(dictionary)
    app.projection = cvt2TJProjection(cameraParameters)
    app.markerDetector = MarkerDetector(dictionary=dictionary, cameraParameters=cameraParameters)

    initArgs(app, PLAYER_RECT=player_rect)

    # Load cameraParameters and dictionary and set markerDetector.
    @app.route('/webar')
    def webar():
        app.args['DEBUG'] = app.config['DEBUG']
        js_tag = int(app.args['DEBUG']) and np.random.randint(0, 1000000)
        return render_template('index.tpl', js_tag=js_tag, args=app.args)

    @app.route('/loadargs')
    def loadArgs():
        return jsonify(app.args)

    # Load b64Frame and find markers matrix.
    @app.route('/loadmodelviews', methods=['POST'])
    def loadModelViews():
        if request.form['b64Frame'] is None: return 'fails'
        b64 = request.form['b64Frame'].encode()
        cvt = base64.b64decode(b64)
        arr = np.frombuffer(base64.b64decode(cvt[22:]), np.uint8)
        frame = cv2.resize(cv2.imdecode(arr, 0), (app.args['PLAYER_RECT'][2], app.args['PLAYER_RECT'][3]))
        markers = app.markerDetector.detect(frame) or []
        modelview_dict = {}
        for marker in markers:
            modelview_dict[marker.marker_id] = cvt2TJModelView(marker)
        return jsonify(modelview_dict)

    return app
