from flask import Flask, render_template, request, jsonify
import base64
import numpy as np
import cv2

from bar4py import Dictionary, CameraParameters, MarkerDetector


class WebAR(Flask):
    def __init__(self, import_name):
        Flask.__init__(self, import_name=import_name)
        self.args = {}
        self.dictionary = None
        self.cameraParameters = None
        self.markerDetector = None

    def initArgs(self, player_rect=None, args={}):
        self.args['PLAYER_RECT'] = player_rect or (0, 35, 640, 480)
        self.args['VISIBLE_TAG'] = 5
        self.args.update(args)

    def setDictionary(self, dictionary, dictionary_opts={}):
        self.dictionary = dictionary
        self.args['DICTIONARY'] = WebAR.cvt2TJDictionary(dictionary, dictionary_opts)

    def setProjection(self, cameraParameters):
        self.cameraParameters = cameraParameters
        self.args['PROJECTION'] = WebAR.cvt2TJProjection(cameraParameters)

    def buildDetector(self):
        if (self.dictionary is None) or (self.cameraParameters is None):
            raise AttributeError('No set dictionary or cameraParameters')
        self.markerDetector = MarkerDetector(dictionary=self.dictionary,
                                             cameraParameters=self.cameraParameters)

    def setDictionaryOptions(self, options):
        self.args['DICTIONARY'].update(options)

    def applyDictionary(self, dictionary, dictionary_opts={}):
        self.setDictionary(dictionary, dictionary_opts)
        self.buildDetector()

    def applycameraParameters(self, cameraParameters):
        self.setProjection(cameraParameters)
        self.buildDetector()

    def detectFromBlob(self, blob):
        array = np.frombuffer(blob, np.uint8)
        if array.shape[0] < 1024: return {}
        frame = cv2.imdecode(array, 0)
        if frame is None: return {}
        frame = cv2.resize(frame, (self.args['PLAYER_RECT'][2], self.args['PLAYER_RECT'][3]))
        markers, area = (self.markerDetector.detect( frame, enFilter=True, enArea=True) or
                         ([], None))
        modelview_dict = {}
        for marker in markers:
            modelview_dict[marker.marker_id] = WebAR.cvt2TJModelView(marker)
        return {'modelview': modelview_dict, 'area': area}

    def run(self, host=None, port=None, debug=None, **options):
        self.args['DEBUG'] = debug
        Flask.run(self, host, port, debug, **options)

    @staticmethod
    def cvt2TJDictionary(dictionary, options):
        tj_dictionary = {marker_id: {'type': 'cube', 'content': None, 'visibleTag': 5}
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
    def cvt2TJModelView(marker, Rx=np.array([[1, 0, 0], [0, -1, 0], [0, 0, -1]])):
        M = marker.cvt2ModelView(Rx)
        return M.flatten().tolist()


def createWebARApp(dictionary, cameraParameters, player_rect=None, app_args={}, dictionary_opts={}):
    app = WebAR(__name__)
    app.initArgs(player_rect, app_args)
    app.setDictionary(dictionary, dictionary_opts)
    app.setProjection(cameraParameters)
    app.buildDetector()

    # Load templates and js scripts
    @app.route('/')
    def index():
        js_tag = int(app.config['DEBUG']) and np.random.randint(0, 99999)
        return render_template('index.tpl', js_tag=js_tag, args=app.args)

    # Init App arguments
    @app.route('/load_args')
    def loadArgs():
        return jsonify(app.args)

    # Load blob to detect markers matrix and area.
    @app.route('/load_modelviews', methods=['POST'])
    def loadModelViews():
        blob = request.data
        modelviews = app.detectFromBlob(blob)
        return jsonify(modelviews)

    return app
