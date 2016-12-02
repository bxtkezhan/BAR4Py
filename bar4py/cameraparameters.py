import numpy as np
import json

class CameraParameters:
    def __init__(self, cameraParametersObj=None,
                 camera_matrix=None, distorsion_coeff=None):
        self.camera_matrix = camera_matrix
        self.distorsion_coeff = distorsion_coeff
        if cameraParametersObj:
            self.camera_matrix = cameraParametersObj.camera_matrix
            self.distorsion_coeff = cameraParametersObj.distorsion_coeff

    def readFromDict(self, parametersDict):
        if parametersDict['cameraMatrix']:
            self.camera_matrix = np.float32(parametersDict['cameraMatrix']).reshape(3,3)
        else:
            self.camera_matrix = None
        if parametersDict['distorsionCoeff']:
            self.distorsion_coeff = np.float32(parametersDict['distorsionCoeff'])
        else:
            self.distorsion_coeff = None

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
        distorsion_coeff = cameraParametersObj.distorsion_coeff
        if isinstance(camera_matrix, np.ndarray):
            parameters['cameraMatrix'] = camera_matrix.flatten().tolist()
        else:
            parameters['cameraMatrix'] = 0
        if isinstance(distorsion_coeff, np.ndarray):
            parameters['distorsionCoeff'] = distorsion_coeff.tolist()
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
