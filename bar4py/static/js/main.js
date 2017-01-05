// App args.
var APP_ARGS;

// Basic objects.
var BG_VIDEO = document.querySelector('video');

// Drawing tools.
var CVT_CANVAS = document.createElement('canvas');
var TEMP_MATRIX = new THREE.Matrix4();

// ThreeJS objects.
var TJ_RENDERER;
var TJ_SCENE;

var TJ_PROJECTION;
var TJ_CAMERA;

var TJ_DICTIONARY;
var TJ_MODELVIEWS;

// Tag values.
var PROC_ID;
var UPDATA_TAG = 0;
var SETUP_STATUS = 0;

// Debug tools.
var DEBUG_MSG_WINDOW = document.querySelector('pre');


function hasUserMedia() { 
	//check if the browser supports the WebRTC 
	return !!(navigator.getUserMedia || navigator.webkitGetUserMedia || 
			navigator.mozGetUserMedia); 
} 

function openWebcamStream() {
	if (hasUserMedia()) { 
		navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia
			|| navigator.mozGetUserMedia; 

		//enabling video and audio channels 
		navigator.getUserMedia({ video: true, audio: false }, function (stream) { 
			//inserting our stream to the video tag     
			BG_VIDEO.srcObject = stream;
			BG_VIDEO.play();
		}, function (err) {}); 
	} else { 
		alert("WebRTC is not supported"); 
	}
}

function loadData(method, url, input, type='dict', asynchronous=true) {
    var xmlhttp = new XMLHttpRequest();
	var output = null;
    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
			switch (type) {
				case 'dict':
					output = JSON.parse(xmlhttp.responseText);
					break;
				case 'list':
					output = JSON.parse(xmlhttp.responseText);
					break;
				default:
					break;
			console.log(output); // Debug code.
			}
        }
    };
    xmlhttp.open(method, url, asynchronous);
	if (method == 'GET') xmlhttp.send();
    else if (method == 'POST') {
		xmlhttp.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded;charset=UTF-8');
		xmlhttp.send(input);
	}
	return output;
}

function initAppArguments() {
	APP_ARGS = loadData('GET', '/initapp', null, 'dict', false);

	BG_VIDEO.width = APP_ARGS.width;
	BG_VIDEO.height = APP_ARGS.height;
	var canvas = document.querySelector('canvas');
	canvas.width = BG_VIDEO.width;
	canvas.height = BG_VIDEO.height;

	TJ_DICTIONARY = APP_ARGS.dictionary;
	TJ_PROJECTION = APP_ARGS.projection;
}

function setup() {
	initAppArguments();

	openWebcamStream();

	TJ_RENDERER = new THREE.WebGLRenderer({
		canvas: document.querySelector('canvas'),
		alpha: true
	});
	TJ_RENDERER.setClearColor(0x000000, 0);

	TJ_CAMERA = new THREE.PerspectiveCamera();
	TJ_CAMERA.projectionMatrix.set(
		TJ_PROJECTION[0], TJ_PROJECTION[1], TJ_PROJECTION[2], TJ_PROJECTION[3],
		TJ_PROJECTION[4], TJ_PROJECTION[5], TJ_PROJECTION[6], TJ_PROJECTION[7],
		TJ_PROJECTION[8], TJ_PROJECTION[9], TJ_PROJECTION[10], TJ_PROJECTION[11],
		TJ_PROJECTION[12], TJ_PROJECTION[13], TJ_PROJECTION[14], TJ_PROJECTION[15]
	);

	TJ_SCENE = new THREE.Scene();

	TJ_SCENE.add(TJ_CAMERA);

	for (var id in TJ_DICTIONARY) {
		TJ_DICTIONARY[id].content = new THREE.Mesh(
			new THREE.CubeGeometry(1, 1, 1),
			new THREE.MeshLambertMaterial({ color: 0x00fffff, wireframe: false })
		);
		TJ_SCENE.add(TJ_DICTIONARY[id].content);
	}

	var lightd = new THREE.DirectionalLight();
	lightd.position.set(0, 0, 5);
	TJ_SCENE.add(lightd);

	CVT_CANVAS.width = BG_VIDEO.width / 2;
	CVT_CANVAS.height = BG_VIDEO.height / 2;
}

function loadModelViewDict() {
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
			TJ_MODELVIEWS = JSON.parse(xmlhttp.responseText);
			// DEBUG_MSG_WINDOW.innerHTML = xmlhttp.responseText;
        }
    };
    CVT_CANVAS.getContext('2d').drawImage(BG_VIDEO, 0, 0, CVT_CANVAS.width, CVT_CANVAS.height);
    xmlhttp.open('POST', '/loadmodelviews', true);
    xmlhttp.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded;charset=UTF-8');
    xmlhttp.send('b64Frame='+btoa(CVT_CANVAS.toDataURL()));
}

function setModelViewByArray(m, a) {
	TEMP_MATRIX.getInverse(m.matrix);
	m.applyMatrix(TEMP_MATRIX);
	TEMP_MATRIX.set(
		a[0], a[1], a[2], a[3],
		a[4], a[5], a[6], a[7],
		a[8], a[9], a[10], a[11],
		a[12], a[13], a[14], a[15]
	);
	m.applyMatrix(TEMP_MATRIX);
	m.translateX(0.5);
	m.translateY(0.5);
	m.translateZ(0.5);
}

function applyModelViewDict() {
	if (TJ_MODELVIEWS == null) return
	for (var id in TJ_DICTIONARY) {
		if (id in TJ_MODELVIEWS) {
			setModelViewByArray(
				TJ_DICTIONARY[id].content,
				TJ_MODELVIEWS[id]
			);
			TJ_DICTIONARY[id].visibleTag = 5;
		} else {
			TJ_DICTIONARY[id].visibleTag--;
		}

		if (TJ_DICTIONARY[id].visibleTag > 0) {
			TJ_DICTIONARY[id].content.visible = true;
		} else {
			TJ_DICTIONARY[id].content.visible = false;
		}
	}
}

function render() {
	TJ_RENDERER.autoClear = false;
	TJ_RENDERER.clear();
	TJ_RENDERER.render(TJ_SCENE, TJ_CAMERA);
}

function draw() {
	if (BG_VIDEO.paused == false && BG_VIDEO.ended == false) {
		loadModelViewDict();
		applyModelViewDict();
		render();
	}
}

function play() {
	if (SETUP_STATUS == 0) {
		setup();
		SETUP_STATUS = 1;
	}
	BG_VIDEO.play();
    window.PROC_ID = setInterval(draw, 50);
}

function stop() {
	BG_VIDEO.pause();
    if (window.PROC_ID != null) {
        clearInterval(window.PROC_ID);
        window.PROC_ID = null;
    }
}
