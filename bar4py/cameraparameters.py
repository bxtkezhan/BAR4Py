import numpy as np
import json

class CameraParameters:
    def __init__(self, cameraParametersObj=None,
                 camera_matrix=None, dist_coeff=None):
        # Default parameters
        self.camera_matrix = camera_matrix
        self.dist_coeff = dist_coeff

        # If input cameraParameters object
        if cameraParametersObj:
            self.camera_matrix = cameraParametersObj.camera_matrix
            self.dist_coeff = cameraParametersObj.dist_coeff

        # Some parameters
        if camera_matrix is not None:
            self.camera_matrix = camera_matrix
        if dist_coeff is not None:
            self.dist_coeff = dist_coeff

    def readFromDict(self, parametersDict):
        if parametersDict['cameraMatrix']:
            self.camera_matrix = np.float32(parametersDict['cameraMatrix']).reshape(3,3)
        else:
            self.camera_matrix = None
        if parametersDict['distorsionCoeff']:
            self.dist_coeff = np.float32(parametersDict['distorsionCoeff'])
        else:
            self.dist_coeff = None

    def readFromJsonString(self, json_string):
        parametersDict = json.loads(json_string)
        self.readFromDict(parametersDict)

    def readFromJsonFile(self, json_filename):
        with open(json_filename) as f:
            parametersDict = json.load(f)
        self.readFromDict(parametersDict)

    def dumpDict(self, cameraParametersObj=None):
        cameraParametersObj = cameraParametersObj or self
        parameters = {}
        camera_matrix = cameraParametersObj.camera_matrix
        dist_coeff = cameraParametersObj.dist_coeff
        if isinstance(camera_matrix, np.ndarray):
            parameters['cameraMatrix'] = camera_matrix.flatten().tolist()
        else:
            parameters['cameraMatrix'] = 0
        if isinstance(dist_coeff, np.ndarray):
            parameters['distorsionCoeff'] = dist_coeff.tolist()
        else:
            parameters['distorsionCoeff'] = 0
        return parameters

    def dumpJsonString(self, cameraParametersObj=None):
        parameters = self.dumpDict(cameraParametersObj)
        return json.dumps(parameters)

    def dumpJsonFile(self, filename, cameraParametersObj=None):
        parameters = self.dumpDict(cameraParametersObj)
        with open(filename, 'w') as f:
            json.dump(parameters, f)
