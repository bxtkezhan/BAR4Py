import sys, os, shutil
from bar4py.shortfuncs import module2path, opjoin

def createWebPlayer(project_name):
    # create project and copy resources to project.
    os.mkdir(project_name)
    base_path = module2path(__file__, '')
    shutil.copy(
        opjoin(base_path, 'resources', 'webplayer.py'),
        opjoin(project_name, 'webplayer.py')
    )
    shutil.copytree(
        opjoin(base_path, 'resources', 'static'),
        opjoin(project_name, 'static')
    )

def main():
    if len(sys.argv) == 3:
        if sys.argv[1] == 'webplayer':
            createWebPlayer(sys.argv[2])
