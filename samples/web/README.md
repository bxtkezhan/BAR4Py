# WebAR Player

**BXT** Augmented Reality For **Python**「**百晓通客栈** `Python`增强现实开发库」

[TOC]

## 效果预览：

[**动图链接../../imgs/weplayer.gif**](../../imgs/webplayer.gif)

## 代码清单：

[**代码文件链接./webplayer.py**](./webplayer.py)

**运行方法：**
```
python3 webplayer.py
```

## 代码解析：

### 创建（标记物）字典对象以及相机参数对象

```python
# Build WebAPP arguments.
dictionary = Dictionary()
dictionary.buildByDirectory(filetype='*.jpg', path=opjoin(RES_MRK, 'batchs'))
cameraParameters = CameraParameters()
cameraParameters.readFromJsonFile(opjoin(RES_CAM, 'camera_640x480.json'))
```

### 创建AR播放器对象

```python
# Create WebAR player.
player = createWebPlayer(__name__, dictionary, cameraParameters,
                         player_rect=(0, 35, 640, 480)) # yapf: disable
```

其中\_\_name\_\_为Python模块名；player\_rect为播放器在浏览器中的绝对位置，分别对应`(left, top, width, height)`

### 配置标记物字典参数

```python
# Set dictionary options
dictionary_opts = {
    '701': {
        'type': 'obj',
        'content': None,
        'mpath': '/static/model/',
        'mname': 'rocket.mtl',
        'opath': '/static/model/',
        'oname': 'rocket.obj',
        'visibleTag': 5
    }
}
player.setDictionaryOptions(dictionary_opts)
```

其中dictionary\_opts的内容形式为`{id: {'type': xxx, 'content': xxx, 'visibleTag`: <整数>, ...}, ...}`

### 设置模型动画脚本

```python
# Set models animate.
animate_js = '''
var RotateTag0 = 0;
var RotateTag1 = 0;
function animate(id, model) {
    if (id == '701') {
        model.rotateX(Math.PI/2);
        model.rotateY(RotateTag0);
        RotateTag0 += 0.1;
    } else if (id == '601') {
        model.translateZ(0.5);
        model.rotateX(RotateTag1);
        RotateTag1 += 0.1;
    }
}
'''
player.setAnimate(animate_js)
```

### 启动Web服务

```python
player.run(port=8000, debug=True)
```

port为端口号，`debug=True`开启调试模式