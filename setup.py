from setuptools import setup, find_packages

exec(open('bar4py/version.py').read())

setup(
    name='bar4py',
    version=__version__,
    author='bxtkezhan-kk',
    author_email='bxtkezhan@qq.com',
    description='Augmented reality lib for Python3',
    url='https://bxtkezhan.github.io/BAR4Py',
    license='MIT License',
    keywords='AR OpenCV',
    packages=find_packages(),
    package_data={'bar4py':[
        'templates/index.tpl',
        'static/js/*.js',
        'resources/*.py',
        'resources/static/animate/*.js',
        'resources/static/camera/*.json',
        'resources/static/dictionary/*.json',
        'resources/static/marker/*.jpg',
        'resources/static/model/*',
    ]},
    install_requires= ['numpy', 'flask'],
    entry_points = {
        'console_scripts': ['bar4py=bar4py.command:main'],
    }
)
