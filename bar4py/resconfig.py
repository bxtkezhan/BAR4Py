import os

# Rename functions

opjoin = os.path.join

# Resources Config

RES_DIR = opjoin(os.path.dirname(os.path.abspath(__file__)), './res')
RES_IMG = opjoin(RES_DIR, 'image')
RES_MRK = opjoin(RES_DIR, 'marker')
RES_VID = opjoin(RES_DIR, 'video')
RES_CAM = opjoin(RES_DIR, 'camera')
