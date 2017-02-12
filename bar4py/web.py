from flask import Flask, render_template_string, request, jsonify
import numpy as np
import cv2

from bar4py.shortfuncs import opjoin, opdirname, opabspath
from bar4py import Dictionary, CameraParameters, MarkerDetector


class WebAPP(Flask):
    '''
    Web Application Class, 2017/1/22 Edit

    Input import_name is module name(__name__)

    For example:
    >>> webApp = WebAPP(__name__)
    '''
    def __init__(self, import_name):
        Flask.__init__(self, import_name=import_name)
        self.args = {}
        self.dictionary = None
        self.cameraParameters = None
        self.markerDetector = None

        with open(opjoin(opdirname(opabspath(__file__)), 'templates/index.tpl')) as f:
            self.template_string = f.read()

        self.js_libs = {}
        static_js_path = opjoin(opdirname(opabspath(__file__)), 'static/js')
        for filename in {'three.min.js', 'MTLLoader.js', 'OBJLoader.js', 'barviews.js'}:
            with open(opjoin(static_js_path, filename)) as f:
                self.js_libs[filename] = open(opjoin(static_js_path, filename)).read()

    def initArgs(self, player_rect=None, args={}):
        '''
        player_rect is WebAR player rect, (left, top, width, height), default is (0, 35, 640, 480)
        args is others options, the type is dict
        
        For example:
        >>> webApp.initArgs(player_rect=(0, 35, 640, 480), args={'APP_TITLE': 'Hello BAR4Py'})
        '''
        self.args['PLAYER_RECT'] = player_rect or (0, 35, 640, 480)
        self.args['VISIBLE_TAG'] = 5
        self.args['APP_TITLE'] = 'Hello BAR4Py'
        self.args.update(args)

    def setDictionary(self, dictionary, dictionary_opts={}):
        '''
        dictionary is BAR4Py.Dictionary object
        dictionary_opts is a dict of models options

        For example:
        >>> webApp.setDictionary(dictionary)
        '''
        self.dictionary = dictionary
        self.args['DICTIONARY'] = WebAPP.cvt2TJDictionary(dictionary, dictionary_opts)

    def setProjection(self, cameraParameters):
        '''
        cameraParameters is BAR4Py.CameraParameters object

        For example:
        >>> webApp.setProjection(cameraParameters)
        '''
        self.cameraParameters = cameraParameters
        self.args['PROJECTION'] = WebAPP.cvt2TJProjection(cameraParameters)

    def buildDetector(self):
        '''
        After set the Dictionary and the Projection

        For example:
        >>> webApp.buildDetector()
        '''
        if (self.dictionary is None) or (self.cameraParameters is None):
            raise AttributeError('No set dictionary or cameraParameters')
        self.markerDetector = MarkerDetector(dictionary=self.dictionary,
                                             cameraParameters=self.cameraParameters)

    def setDictionaryOptions(self, options):
        '''
        Reset the dictionary model options
        options is a dict of model options

        For example:
        >>> webApp.setDictionaryOptions({
        >>>     '701': {
        >>>         'type': 'obj',
        >>>         'content': None,
        >>>         'mpath': '/static/model/',
        >>>         'mname': 'mk.mtl',
        >>>         'opath': '/static/model/',
        >>>         'oname': 'mk.obj',
        >>>         'visibleTag': 5
        >>>     }
        >>> })
        '''
        self.args['DICTIONARY'].update(options)

    def applyDictionary(self, dictionary, dictionary_opts={}):
        '''
        Apply new BAR4Py.Dictionary object
        dictionary is BAR4Py.Dictionary object
        dictionary_opts is options of models

        For example:
        >>> webApp.applyDictionary(dictionary)
        '''
        self.setDictionary(dictionary, dictionary_opts)
        self.buildDetector()

    def applycameraParameters(self, cameraParameters):
        '''
        Apply new BAR4Py.CameraParameters object
        cameraParameters is BAR4Py.CameraParameters object

        For example:
        >>> webApp.applycameraParameters(cameraParameters)
        '''
        self.setProjection(cameraParameters)
        self.buildDetector()

    def detectFromBlob(self, blob):
        '''
        Detect markers from web blob
        blob is image blob, type is bytes

        For example:
        >>> modelviews = webApp.detectFromBlob(blob)
        '''
        array = np.frombuffer(blob, np.uint8)
        if array.shape[0] < 1024: return {}
        frame = cv2.imdecode(array, 0)
        if frame is None: return {}
        frame = cv2.resize(frame, (self.args['PLAYER_RECT'][2], self.args['PLAYER_RECT'][3]))
        markers, area = (self.markerDetector.detect( frame, enFilter=True, enArea=True) or
                         ([], None))
        modelview_dict = {}
        for marker in markers:
            modelview_dict[marker.marker_id] = WebAPP.cvt2TJModelView(marker)
        return {'modelview': modelview_dict, 'area': area}

    def setAnimate(self, animate_js):
        '''
        Set WebAR model animate javascript

        For example:
        >>> webApp.setAnimate(animate_js)
        '''
        self.args['ANIMATEJS'] = animate_js
        self.args['ENANIMATE'] = True

    def deleteAnimate(self):
        '''
        Clear WebAR model animate javascript

        For example:
        >>> webApp.deleteAnimate()
        '''
        self.args['ANIMATEJS'] = ''
        self.args['ENANIMATE'] = False

    def run(self, host=None, port=None, debug=None, **options):
        '''
        WebAPP.run like Flask.run
        '''
        self.args['DEBUG'] = debug
        Flask.run(self, host, port, debug, **options)

    @staticmethod
    def cvt2TJDictionary(dictionary, options):
        '''
        Convert dictionary and options to tj_dictionary
        dictionary is BAR4Py.Dictionary object
        options is a dict of model options

        For example:
        >>> tj_dictionary = webApp.cvt2TJDictionary(dictionary, options)
        '''
        tj_dictionary = {marker_id: {'type': 'cube', 'content': None, 'visibleTag': 5}
                         for marker_id in dictionary.ids}
        for _id in options.keys():
            if _id in tj_dictionary:
                tj_dictionary[_id].update(options[_id])
        return tj_dictionary

    @staticmethod
    def cvt2TJProjection(cameraParameters):
        '''
        Convert cameraParameters to tj_projection
        cameraParameters is BAR4Py.CameraParameters object

        For example:
        >>> p_lst = webApp.setProjection(cameraParameters)
        '''
        P = cameraParameters.cvt2Projection()
        return P.flatten().tolist()

    @staticmethod
    def cvt2TJModelView(marker, Rx=np.array([[1, 0, 0], [0, -1, 0], [0, 0, -1]])):
        '''
        Convert marker modelview matrix to tj_modelview
        marker is BAR4Py.Marker object

        For example:
        >>> modelview_lst = webApp.cvt2TJModelView(marker)
        '''
        M = marker.cvt2ModelView(Rx)
        return M.flatten().tolist()


def createWebPlayer(import_name, dictionary, cameraParameters, player_rect=None, app_args={}, dictionary_opts={}):
    '''
    Create Web AR player

    Inputs:
    import_name is module name(__name__)
    dictionary is BAR4Py.Dictionary object
    cameraParameters is BAR4Py.CameraParameters object
    player_rect is the Web AR player rect, type is tuple, default (0, 35, 640, 480)
    app_args is WebAPP object args, type is dict
    dictionary_opts is model options, type is dict

    For example:
    >>> player = createWebPlayer(__name__, dictionary, cameraParameters, (0, 35, 640, 480))
    '''
    app = WebAPP(import_name)
    app.initArgs(player_rect, app_args)
    app.setDictionary(dictionary, dictionary_opts)
    app.setProjection(cameraParameters)
    app.buildDetector()

    # Load template
    @app.route('/')
    def index():
        return render_template_string(app.template_string, args=app.args)

    # Load javascript libs
    @app.route('/jslibs/<filename>')
    def jsLibs(filename):
        return app.js_libs[filename]

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

    # Default animates.
    @app.route('/animates')
    def animates():
        return app.args['ANIMATEJS']

    return app
