import numpy as np
import json

class CameraParameters:
    '''
    CameraParameters Class, 2016/12/10 Edit

    Inputs:
    cameraParametersObj is CameraParameters object
    Type of camera_matrix is np.ndarray, and shape of points is (3,3)
    Type of dist_coeff is np.ndarray

    For examples:
    >>> from bar4py.camereparameters import CameraParameters
    >>> cameraParameters = CameraParameters()
    >>> cameraParameters = CameraParameters(cameraParameters)
    >>> cameraParameters = CameraParameters(camera_matrix=camera_matrix)
    >>> cameraParameters = CameraParameters(camera_matrix=camera_matrix, dist_coeff=dist_coeff)
    >>> cameraParameters = CameraParameters(cameraParametersObj, camera_matrix=camera_matrix, dist_coeff=dist_coeff)
    '''
    def __init__(self, cameraParametersObj=None,
                 camera_matrix=None, dist_coeff=None, size=None):
        # Default parameters
        self.camera_matrix = None
        self.dist_coeff = np.zeros((4,), dtype=np.float32)
        self.size = None

        # If input cameraParameters object
        if cameraParametersObj:
            self.camera_matrix = cameraParametersObj.camera_matrix
            self.dist_coeff = cameraParametersObj.dist_coeff

        # Some parameters
        if camera_matrix is not None:
            self.camera_matrix = camera_matrix
        if dist_coeff is not None:
            if len(dist_coeff) not in (4,5):
                raise TypeError('Bad dist_coeff, the length of dist_coeff is 4 or 5')
            self.dist_coeff = dist_coeff
        if size is not None:
            if len(size) != 2:
                raise TypeError('The size is (width, height)')
            self.size = tuple(size)

    def readFromDict(self, parametersDict):
        '''
        parametersDict is cameraParameters dump to dict
        Set camera_matrix and dist_coeff by parametersDict
        '''
        if parametersDict['cameraMatrix']:
            self.camera_matrix = np.float32(parametersDict['cameraMatrix']).reshape(3,3)
        else:
            self.camera_matrix = None
        if parametersDict['distorsionCoeff']:
            if len(self.dist_coeff) not in (4,5):
                raise TypeError('Bad dist_coeff, the length of dist_coeff is 4 or 5')
            self.dist_coeff = np.float32(parametersDict['distorsionCoeff'])
        else:
            self.dist_coeff = None
        if 'size' in parametersDict:
            if len(parametersDict['size']) != 2:
                raise TypeError('The size is (width, height)')
            self.size = tuple(parametersDict['size'])

    def readFromJsonString(self, json_string):
        '''
        json_string is cameraParameters dump to json
        Set camera_matrix and dist_coeff by json_string
        '''
        parametersDict = json.loads(json_string)
        self.readFromDict(parametersDict)

    def readFromJsonFile(self, json_filename):
        '''
        json_filename is CameraParameters dump to json file
        Set camera_matrix and dist_coeff by json file
        '''
        with open(json_filename) as f:
            parametersDict = json.load(f)
        self.readFromDict(parametersDict)

    def dumpDict(self, cameraParametersObj=None):
        '''
        cameraParametersObj is CameraParameters object
        return parameters(type is dict)
        '''
        cameraParametersObj = cameraParametersObj or self
        parameters = {}
        camera_matrix = cameraParametersObj.camera_matrix
        dist_coeff = cameraParametersObj.dist_coeff
        size = cameraParametersObj.size
        if isinstance(camera_matrix, np.ndarray):
            parameters['cameraMatrix'] = camera_matrix.flatten().tolist()
        else:
            parameters['cameraMatrix'] = 0
        if isinstance(dist_coeff, np.ndarray):
            parameters['distorsionCoeff'] = dist_coeff.tolist()
        else:
            parameters['distorsionCoeff'] = 0
        if isinstance(size, tuple):
            parameters['size'] = size
        return parameters

    def dumpJsonString(self, cameraParametersObj=None):
        '''
        cameraParametersObj is CameraParameters object
        return parameters(type is json string)
        '''
        parameters = self.dumpDict(cameraParametersObj)
        return json.dumps(parameters)

    def dumpJsonFile(self, filename, cameraParametersObj=None):
        '''
        filename is saveing file path
        cameraParametersObj is CameraParameters object
        cameraParameters save to file
        '''
        parameters = self.dumpDict(cameraParametersObj)
        with open(filename, 'w') as f:
            json.dump(parameters, f)

    def cvt2Projection(self, imgsize=None, near=0.01, far=100):
        if self.camera_matrix is None:
            raise TypeError('No set the camera_matrix')
        if (imgsize is None) and (self.size is None):
            raise TypeError('No set the size, imgsize is None and camsize is None')

        imgsize = imgsize or self.size
        camsize = self.size or imgsize
        ax = camsize[0] / imgsize[0]
        ay = camsize[1] / imgsize[1]
        print(ax, ay)

        fx = self.camera_matrix[0, 0] * ax
        fy = self.camera_matrix[1, 1] * ay
        cx = self.camera_matrix[0,-1] * ax
        cy = self.camera_matrix[1,-1] * ay

        width, height = camsize
        P = np.zeros((4,4), dtype=np.float32)
        P[0, 0] = 2 * fx / width
        P[1, 1] = 2 * fy / height
        P[0, 2] = 1 - (2 * cx / width)
        P[1, 2] = (2 * cy / height) - 1
        P[2, 2] = -(far + near) / (far - near)
        P[3, 2] = -1
        P[2, 3] = -(2 * far * near) / (far - near)

        return P

    def cvt2GLProjection(self, imgsize=None, near=0.01, far=100):
        P = self.cvt2Projection(imgsize, near, far)
        return P.T.flatten()
