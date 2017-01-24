# Preview Core

**BXT** Augmented Reality For **Python**「**百晓通客栈** `Python`增强现实开发库」

[TOC]

## 效果预览：

[**动图链接../../imgs/core_preview.gif**](../../imgs/core_preview.gif)

## 代码清单：

[**代码文件链接./preview_core.py**](./preview_core.py)

**运行方法：**
```
python3 preview_core.py
```

## 代码解析：

### OpenCV 直接相关的代码部分

参考 PyOpenCV 文档 [**http://opencv-python-tutroals.readthedocs.io/en/latest/index.html**](http://opencv-python-tutroals.readthedocs.io/en/latest/index.html)

### 创建相机参数、（标记物）字典对象，并构建（标记物）检测器

```python
    # Load Camera Parameters
    cameraParameters = CameraParameters()
    cameraParameters.readFromJsonFile(opjoin(RES_CAM, 'camera_640x480.json'))
    print('GLPV:', cameraParameters.cvt2GLProjection((640, 480)).tolist())
    # Create Dictionary
    dictionary = Dictionary()
    dictionary.buildByDirectory(filetype='*.jpg', path=RES_MRK)
    # Create MarkerDetector
    markerDetector = MarkerDetector(dictionary=dictionary, cameraParameters=cameraParameters)
```

### 检测标记物信息（ID，位置，视图矩阵，区域范围等）

```python
        markers, area = markerDetector.detect(frame, enArea=True)
```

其中markers为BAR4Py的Marker对象组成的Python列表结构；area是一个存贮区域信息的Python元祖结构，分别对应`(left, top, right, bottom)`

**注意：**其中`enArea=True`表示开启检测器对所有标记物区域范围的估计，默认为False且当其为False的时候detect方法仅返回markers，`markers = markerDetector.detect(frame)`