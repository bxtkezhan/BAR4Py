<html>
<head>
	<meta charset="utf-8">
	<script type="text/javascript" src="{{ url_for('static', filename='js/three.min.js') }}"></script>
	<script type="text/javascript" src="{{ url_for('static', filename='js/MTLLoader.js') }}"></script>
	<script type="text/javascript" src="{{ url_for('static', filename='js/OBJLoader.js') }}"></script>
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
{% if args.DEBUG %}
<script type="text/javascript" src="{{ url_for('static', filename='js/barviews.js') }}?id={{ js_tag }}"></script>
{% else %}
<script type="text/javascript" src="{{ url_for('static', filename='js/barviews.js') }}"></script>
{% endif %}
{% if args.ENANIMATE %}
<script type="text/javascript" src="{{ url_for('animates') }}"></script>
{% endif %}
