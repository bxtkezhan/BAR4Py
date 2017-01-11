from flask import Flask, render_template, request, jsonify
import base64
import numpy as np
import cv2

from bar4py import Dictionary, CameraParameters, MarkerDetector


class WebAR(Flask):
    def __init__(self, import_name, dictionary, cameraParameters, player_rect=None, **args):
        Flask.__init__(self, import_name=import_name)
        if not hasattr(self, 'args'): self.args = {}
        self.args['DICTIONARY'] = WebAR.cvt2TJDictionary(dictionary)
        self.args['PROJECTION'] = WebAR.cvt2TJProjection(cameraParameters)
        self.args['PLAYER_RECT'] = player_rect or (0, 35, 640, 480)
        self.args.update(args)
        self.makeDetector(dictionary, cameraParameters)

    def makeDetector(self, dictionary=None, cameraParameters=None):
        self.markerDetector = MarkerDetector(dictionary=dictionary, cameraParameters=cameraParameters)

    def detectFromBlob(self, blob):
        array = np.frombuffer(blob, np.uint8)
        if array.shape[0] < 1024: return {}
        frame = cv2.imdecode(array, 0)
        if frame is None: return {}
        frame = cv2.resize(frame, (self.args['PLAYER_RECT'][2], self.args['PLAYER_RECT'][3]))
        markers, area = (self.markerDetector.detect(frame, enFilter=True, enArea=True) or
                         ([], None))
        modelview_dict = {}
        for marker in markers:
            modelview_dict[marker.marker_id] = WebAR.cvt2TJModelView(marker)
        return {'modelview': modelview_dict, 'area': area}

    def run(self, host=None, port=None, debug=None, **options):
        self.args['DEBUG'] = debug
        Flask.run(self, host, port, debug, **options)

    @staticmethod
    def cvt2TJDictionary(dictionary, **options):
        tj_dictionary = {marker_id: {'type': 'cube', 'content': None, 'visibleTag': 3}
                         for marker_id in dictionary.ids}
        for _id in options.keys():
            if _id in tj_dictionary:
                tj_dictionary[_id].update(options[_id])
        return tj_dictionary

    @staticmethod
    def cvt2TJProjection(cameraParameters):
        P = cameraParameters.cvt2Projection()
        return P.flatten().tolist()

    @staticmethod
    def cvt2TJModelView(marker, Rx=np.array([[1,0,0],[0,-1,0],[0,0,-1]])):
        M = marker.cvt2ModelView(Rx)
        return M.flatten().tolist()

def createWebARApp(dictionary, cameraParameters, player_rect, **args):
    app = WebAR(__name__, dictionary, cameraParameters, player_rect, **args)

    # Load templates and js scripts
    @app.route('/webar')
    def webar():
        js_tag = int(app.config['DEBUG']) and np.random.randint(0, 99999)
        return render_template('index.tpl', js_tag=js_tag, args=app.args)

    # Init App arguments
    @app.route('/loadargs')
    def loadArgs():
        return jsonify(app.args)

    # Load b64Frame and find markers matrix.
    @app.route('/loadmodelviews', methods=['POST'])
    def loadModelViews():
        blob = request.data
        modelview_dict = app.detectFromBlob(blob)
        return jsonify(modelview_dict)

    return app
