#! /usr/bin/env python3
from bar4py.shortfuncs import opjoin
from bar4py import Dictionary, CameraParameters, createWebPlayer

# Configs.
CONFIG = {
    'app_name': 'Hello BAR4Py',
    'marker_path': './static/marker',
    'marker_type': '*.jpg',
    'camera_file': './static/camera/camera_640x480.json',
    'dictionary_file': './static/dictionary/dictionary.json',
    'animate_file': './static/animate/animate.js',
    'port': 8000,
    'debug': False,
}

# Build WebAPP arguments.
dictionary = Dictionary()
dictionary.buildByDirectory(
    filetype=CONFIG['marker_type'],
    path=CONFIG['marker_path']
) # yapf: disable
cameraParameters = CameraParameters()
cameraParameters.readFromJsonFile(CONFIG['camera_file'])

# Create WebAR player.
player = createWebPlayer(__name__, dictionary, cameraParameters,
                         player_rect=(0, 35, 640, 480),
                         app_args={'APP_TITLE': CONFIG['app_name']}) # yapf: disable

# Set dictionary options
import json
with open(CONFIG['dictionary_file'], 'r') as f:
    dictionary_opts = json.load(f)
player.setDictionaryOptions(dictionary_opts)

# Set models animate.
with open(CONFIG['animate_file'], 'r') as f:
    animate_js = f.read()
player.setAnimate(animate_js)

if __name__ == '__main__': player.run(port=CONFIG['port'], debug=CONFIG['debug']) # yapf: disable
