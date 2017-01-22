// App args.
var APP_ARGS;

// Basic objects.
var CAM_VIDEO = document.createElement('video');
var BG_CANVAS = document.getElementById('BG_CANVAS');
var TJ_CANVAS = document.getElementById('TJ_CANVAS');

// Drawing tools.
var CVT_CANVAS = document.createElement('canvas');
var TMP_MATRIX = new THREE.Matrix4();

// ThreeJS objects.
var TJ_RENDERER;
var TJ_SCENE;

var TJ_PROJECTION;
var TJ_CAMERA;

var TJ_DICTIONARY;
var TJ_MODELVIEWS;

var TJ_LIGHTS;

// Tag values.
var SETUP_STATUS = 0;
var PROC_ID;
var VISIBLE_TAG;
var MK_AREA;

// Commen data loader
function loadData(method, url, input, asynchronous=true) {
    var xmlhttp = new XMLHttpRequest();
	var output = null;
    xmlhttp.onload = function(e) {
        if (this.status == 200 || this.status == 304) {
			output = JSON.parse(this.responseText);
        }
    };
    xmlhttp.open(method, url, asynchronous);
	if (method == 'GET') xmlhttp.send();
    else if (method == 'POST') {
		xmlhttp.send(input);
	}
	return output;
}

// Load OBJ model
function loadOBJ(item) {
	var opath = item.opath;
	var oname = item.oname;
	var objLoader = new THREE.OBJLoader();
	objLoader.setPath(opath);
	objLoader.load(oname, function ( object ) {
			item.content = object;
		}, 
		function (xhr) {}, function (xhr) {}
	);
}

// Load MTL OBJ model
function loadMTLOBJ(item) {
	var mpath = item.mpath;
	var mname = item.mname;
	var opath = item.opath;
	var oname = item.oname;
	var mtlLoader = new THREE.MTLLoader();
	mtlLoader.setPath(mpath);
	mtlLoader.load(mname, function( materials) {
		materials.preload();
		var objLoader = new THREE.OBJLoader();
		objLoader.setMaterials( materials );
		objLoader.setPath(opath);
		objLoader.load(oname, function ( object ) {
			item.content = object;
		}, function (xhr) {}, function (xhr) {} );
	});
}

// Valid Webcam
function hasUserMedia() { 
	//check if the browser supports the WebRTC 
	return !!(navigator.getUserMedia || navigator.webkitGetUserMedia || 
			navigator.mozGetUserMedia); 
} 

// Open Webcam
function openWebcamStream() {
	if (hasUserMedia()) { 
		navigator.getUserMedia = navigator.getUserMedia ||
								 navigator.webkitGetUserMedia ||
								 navigator.mozGetUserMedia; 
		//enabling video and audio channels 
		navigator.getUserMedia({ video: true, audio: false }, function (stream) { 
			//inserting our stream to the video tag     
			CAM_VIDEO.srcObject = stream;
		}, function (err) {}); 
	} else { 
		alert("WebRTC is not supported"); 
		window.location.href = '/';
	}
}

// Add tj-camera object
function addCamera(projection, scene) {
	camera = new THREE.PerspectiveCamera();
	camera.projectionMatrix.set(
		projection[0], projection[1], projection[2], projection[3],
		projection[4], projection[5], projection[6], projection[7],
		projection[8], projection[9], projection[10], projection[11],
		projection[12], projection[13], projection[14], projection[15]
	);
	scene.add(camera);
	return camera;
}

// Add tj-model objects
function addModels(dictionary, scene) {
	for (var id in dictionary) {
		scene.add(dictionary[id].content);
	}
}

// Add tj-lights object
function addLights(scene) {
	var lights = new THREE.DirectionalLight();
	lights.position.set(0, 0, 5);
	scene.add(lights);
	return lights;
}

// Create tj renderer
function createRenderer(canvas) {
	renderer = new THREE.WebGLRenderer({
		canvas: canvas,
		alpha: true
	});
	renderer.setClearColor(0x000000, 0);
	return renderer;
}

// Deal modelviews
function updateModelViewAndArea() {
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onload = function(e) {
        if (this.status == 200 || this.status == 304) {
			resObj = JSON.parse(this.responseText);
			TJ_MODELVIEWS = resObj.modelview;
			MK_AREA = resObj.area;
        }
    };
	var context = CVT_CANVAS.getContext('2d');
    context.drawImage(CAM_VIDEO, 0, 0, BG_CANVAS.width, BG_CANVAS.height);
	if (MK_AREA != null) {
		context.clearRect(0, 0, MK_AREA[2], MK_AREA[1]);
		context.clearRect(MK_AREA[2], 0, BG_CANVAS.width, MK_AREA[3]);
		context.clearRect(MK_AREA[0], MK_AREA[3], BG_CANVAS.width, BG_CANVAS.height);
		context.clearRect(0, MK_AREA[1], MK_AREA[0], BG_CANVAS.height);
	}
    xmlhttp.open('POST', '/load_modelviews', true);
	CVT_CANVAS.toBlob(function (b) { window.CVT_BLOB = b; }, 'image/jpeg');
    xmlhttp.send(window.CVT_BLOB);
}

// Set ModelView
function setModelViewByArray(m, a) {
	TMP_MATRIX.getInverse(m.matrix);
	m.applyMatrix(TMP_MATRIX);
	TMP_MATRIX.set(
		a[0], a[1], a[2], a[3],
		a[4], a[5], a[6], a[7],
		a[8], a[9], a[10], a[11],
		a[12], a[13], a[14], a[15]
	);
	m.applyMatrix(TMP_MATRIX);
	m.translateX(0.5);
	m.translateY(0.5);
	m.translateZ(0.5);
}

// Deal ModelViewDict object
function applyModelViewDict() {
	if (TJ_MODELVIEWS == null) return
	for (var id in TJ_DICTIONARY) {
		if (id in TJ_MODELVIEWS) {
			setModelViewByArray(
				TJ_DICTIONARY[id].content,
				TJ_MODELVIEWS[id]
			);
			TJ_DICTIONARY[id].visibleTag = VISIBLE_TAG;
			if (window.animate != null) {
				animate(id, TJ_DICTIONARY[id].content);
			}
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

// Render WebGL
function render() {
	TJ_RENDERER.autoClear = false;
	TJ_RENDERER.clear();
	TJ_RENDERER.render(TJ_SCENE, TJ_CAMERA);
}

// AR Player setup
function setup() {
	openWebcamStream();

	TJ_SCENE = new THREE.Scene();

	TJ_CAMERA = addCamera(TJ_PROJECTION, TJ_SCENE);

	addModels(TJ_DICTIONARY, TJ_SCENE);

	TJ_LIGHTS = addLights(TJ_SCENE);

	TJ_RENDERER = createRenderer(TJ_CANVAS);
}

// AR Player draw
function draw() {
	if (CAM_VIDEO.paused == false && CAM_VIDEO.ended == false) {
		BG_CANVAS.getContext('2d').drawImage(CAM_VIDEO, 0, 0);
		updateModelViewAndArea();
		applyModelViewDict();
		render();
	}
}

// Init app arguments
function initAppArguments() {
	APP_ARGS = loadData('GET', '/load_args', null, false);

	BG_CANVAS.width = APP_ARGS.PLAYER_RECT[2];
	BG_CANVAS.height = APP_ARGS.PLAYER_RECT[3];

	TJ_CANVAS.width = BG_CANVAS.width;
	TJ_CANVAS.height = BG_CANVAS.height;

	CVT_CANVAS.width = Math.floor(BG_CANVAS.width * 0.625);
	CVT_CANVAS.height = Math.floor(BG_CANVAS.height * 0.625);
	CVT_CANVAS.getContext('2d').scale(0.625, 0.625);

	TJ_DICTIONARY = APP_ARGS.DICTIONARY;
	TJ_PROJECTION = APP_ARGS.PROJECTION;

	VISIBLE_TAG = APP_ARGS.VISIBLE_TAG;
}

// AR Player Main.

initAppArguments();

// Preload OBJ models
function preload(dictionary) {
	for (var id in dictionary) {
		switch (dictionary[id].type) {
			case 'plane':
				dictionary[id].content = new THREE.Mesh(
					new THREE.PlaneGeometry(1, 1),
					new THREE.MeshLambertMaterial({ color: 0x00ffff, wireframe: false })
				);
				break;
			case 'sphere':
				dictionary[id].content = new THREE.Mesh(
					new THREE.SphereGeometry(0.5, 20, 20),
					new THREE.MeshLambertMaterial({ color: 0x00ffff, wireframe: false })
				);
				break;
			case 'cylinder':
				dictionary[id].content = new THREE.Mesh(
					new THREE.CylinderGeometry(0.5, 0.5, 1, 20),
					new THREE.MeshLambertMaterial({ color: 0x00ffff, wireframe: false })
				);
				break;
			case 'torus':
				dictionary[id].content = new THREE.Mesh(
					new THREE.TorusGeometry(0.5, 0.25, 20, 20),
					new THREE.MeshLambertMaterial({ color: 0x00ffff, wireframe: false })
				);
				break;
			case 'obj':
				if (dictionary[id]['mpath'] == null || dictionary[id]['mname'] == null) {
					loadOBJ(dictionary[id]);
				} else {
					loadMTLOBJ(dictionary[id]);
				}
				break;
			default:
				dictionary[id].content = new THREE.Mesh(
					new THREE.CubeGeometry(1, 1, 1),
					new THREE.MeshLambertMaterial({ color: 0x00ffff, wireframe: false })
				);
				break;
		}
	}
}

preload(TJ_DICTIONARY);

// AR Player Controls
function play() {
	if (SETUP_STATUS == 0) {
		setup();
		SETUP_STATUS = 1;
	}
	if (window.PROC_ID == null) {
		CAM_VIDEO.play();
		window.PROC_ID = setInterval(draw, 50);
	}
}

function stop() {
	CAM_VIDEO.pause();
    if (window.PROC_ID != null) {
        clearInterval(window.PROC_ID);
        window.PROC_ID = null;
    }
}
