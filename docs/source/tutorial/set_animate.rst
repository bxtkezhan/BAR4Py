自定义动画
================

现在我们要来完成自定义动画的操作了。在自定义动画的操作中我们会用到 Javascript 编程语言，\
还有 Three.JS 库的一些方法。

创建并编辑动画脚本
-----------------------

我们在一个地方创建一个名叫 animate.js 的脚本，然后写入如下内容::

    var RotateTag = 0;
    function animate(id, model) {
        if (id == '701') {
            model.rotateX(Math.PI/2);
            model.rotateY(RotateTag);
            RotateTag += 0.1;
        }
    }

这里先解释一下该段 Javascript 代码。首先我们需要在我们的动画脚本文件当中定义一个名叫 animate 的函数，\
且该函数接受两个参数变量（这个是固定的，必须如此），第一个参数是当前被检测到的标记物的 ID，
第二个参数是当前被检测到的标记物所对应的模型对象；有了 ID 和 模型对象，我们就可以通过 Three.JS 的方法\
去定义模型的动画了´ ▽ ` )ﾉ。

关于 Three.JS 的方法大家可以去往 Three.JS 的官网阅读文档，KK这里就不多说了(｢・ω・)｢～～～

在 ``CONFIG`` 中指定动画脚本文件路径
------------------------------------------

我们可以在 WebARPlayer 的主脚本的 ``CONFIG`` 中，设置 ``'animate_file'`` 的值来指定动画脚本::

    # Configs.
    CONFIG = {
        ...

        'animate_file': './static/animate/animate.js',

        ...
    }

好了，至此我们已经完成了自定义动画的操作了´ ▽ ` )ﾉ～～～！！！
