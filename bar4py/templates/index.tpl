<html>
    <head>
        <meta charset="utf-8">
<style>
body { margin: 0px; padding: 0px }
video, canvas {
	position: absolute;
	top: {{ args.top }}px;
	left: {{ args.left }}px;
}
pre { position: absolute; top: {{ args.top + args.height }}px }
</style>

    </head>
<body>
	<button onclick="play()"> play </button>
	<button onclick="stop()"> stop </button>
	<!--video src="{{ url_for('static', filename='video/video.mp4') }}"></video-->
	<video></video>
	<canvas></canvas>
	<pre></pre>
</body>
</html>

<script type="text/javascript" src="{{ url_for('static', filename='js/three.min.js') }}"></script>
<script type="text/javascript" src="{{ url_for('static', filename='js/main.js') }}?id={{ js_tag }}"></script>
