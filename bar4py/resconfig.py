from bar4py.shortfuncs import opjoin, module2path

# Resources Config

RES_DIR = module2path(__file__, 'res')
RES_IMG = opjoin(RES_DIR, 'image')
RES_MRK = opjoin(RES_DIR, 'marker')
RES_VID = opjoin(RES_DIR, 'video')
RES_CAM = opjoin(RES_DIR, 'camera')
