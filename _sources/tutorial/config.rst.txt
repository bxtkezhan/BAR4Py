修改配置
============

下面KK开始介绍配置这个 WebAR 播放器的方法。

配置文件
-------------

找到主脚本 webplayer.py 的配置变量 ``CONFIG`` ，大概从第五行开始就是了，代码内容大致如下::

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

我们可以尝试修改该 `python` 字典来配置我们的 WebAR 播放器。

配置项说明
--------------

* ``'app_name': 'XXX'`` 用于设置 WebAR 播放器页面的Title
* ``'marker_path': 'XXX'`` 用于指定 marker 标记物图片所在目录
* ``'marker_type': '*.XXX'`` 用于指定 marker 标记物图片的扩展名
* ``'camera_file': 'XXX'`` 用于指定相机参数文件路径
* ``'dictionary_file': 'XXX'`` 用于指定字典内容文件路径
* ``'animate_file': 'XXX'`` 用于指定动画脚步文件路径
* ``'port': XXX`` 用于设置服务端程序端口号
* ``'debug': True/False`` 是否开启调试模式
