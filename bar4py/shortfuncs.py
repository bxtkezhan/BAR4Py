import cv2
import numpy as np

# Short Way

bgr2rgb = lambda I: cv2.cvtColor(I, cv2.COLOR_BGR2RGB)
bgr2gray = lambda I: cv2.cvtColor(I, cv2.COLOR_BGR2GRAY)

