<html>
<head>
	<meta charset="utf-8">
	<title>{{ args.APP_TITLE }}</title>
	<script type="text/javascript" src="{{ url_for('jsLibs', filename='three.min.js') }}"></script>
	<script type="text/javascript" src="{{ url_for('jsLibs', filename='MTLLoader.js') }}"></script>
	<script type="text/javascript" src="{{ url_for('jsLibs', filename='OBJLoader.js') }}"></script>
	<style>
	body { margin: 0px; padding: 0px }
	canvas { position: absolute; left: {{ args.PLAYER_RECT[0] }}px; top: {{ args.PLAYER_RECT[1] }}px; }
	</style>
</head>
<body>
	<button onclick="play()"> Play </button>
	<button onclick="stop()"> Stop </button>
	<canvas id="BG_CANVAS"></canvas>
	<canvas id="TJ_CANVAS"></canvas>
</body>
</html>
<script type="text/javascript" src="{{ url_for('jsLibs', filename='barviews.js') }}"></script>
<script type="text/javascript" src="{{ url_for('animates') }}"></script>
