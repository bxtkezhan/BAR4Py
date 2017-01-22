# Python lib short way

import os

opjoin = os.path.join
opdirname = os.path.dirname
opabspath = os.path.abspath
module2path = lambda f, d: opjoin(os.path.dirname(os.path.abspath(f)), d)
filename2basename = lambda f: os.path.basename(f).split('.')[0]

# OpenCV short way

import cv2

bgr2rgb = lambda I: cv2.cvtColor(I, cv2.COLOR_BGR2RGB)
bgr2gray = lambda I: cv2.cvtColor(I, cv2.COLOR_BGR2GRAY)
