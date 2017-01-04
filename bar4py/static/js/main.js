// Basic objects.
var BG_VIDEO = document.querySelector('video');

// Drawing tools.
var CVT_CANVAS = document.createElement('canvas');
var TEMP_MATRIX = new THREE.Matrix4();

// ThreeJS objects.
var TJ_RENDERER;
var TJ_CAMERA;
var TJ_SCENE;
var TJ_MODEL_OBJ_LIST = [1,2,3,4,5,6];
var TJ_MODEL_MTX_LIST = [];

// Tag values.
var PROC_ID;
var UPDATA_TAG = 0;
var SETUP_STATUS = 0;

// Debug tools.
var DEBUG_MSG_WINDOW = document.querySelector('pre');

function setup() {
	TJ_RENDERER = new THREE.WebGLRenderer({
		canvas: document.querySelector('canvas'),
		alpha: true
	});
	TJ_RENDERER.setClearColor(0x000000, 0);

	TJ_CAMERA = new THREE.PerspectiveCamera();
	TJ_CAMERA.projectionMatrix.set(1.962993860244751, 0.0, -0.012809371575713158, 0.0, 0.0, 2.617316722869873, 0.08711662143468857, 0.0, 0.0, 0.0, -1.0002000331878662, -0.020002000033855438, 0.0, 0.0, -1.0, 0.0);

	TJ_SCENE = new THREE.Scene();

	TJ_SCENE.add(TJ_CAMERA);

	for (var i=0; i<TJ_MODEL_OBJ_LIST.length; i++) {
		TJ_MODEL_OBJ_LIST[i] = new THREE.Mesh(
			new THREE.CubeGeometry(1, 1, 1),
			new THREE.MeshLambertMaterial({ color: 0x00fffff, wireframe: false })
		);
		TJ_SCENE.add(TJ_MODEL_OBJ_LIST[i]);
	}

	var lightd = new THREE.DirectionalLight();
	lightd.position.set(0, 0, 5);
	TJ_SCENE.add(lightd);

	CVT_CANVAS.width = BG_VIDEO.width / 2;
	CVT_CANVAS.height = BG_VIDEO.height / 2;
}

function render() {
	TJ_RENDERER.autoClear = false;
	TJ_RENDERER.clear();
	TJ_RENDERER.render(TJ_SCENE, TJ_CAMERA);
}

function draw() {
	/*
	if (UPDATA_TAG > 0) {
		cube.visible = true;
	} else {
		cube.visible = false;
	}
	*/
	render();
}

function updateCube(mlist) {
	TEMP_MATRIX.getInverse(cube.matrix);
	cube.applyMatrix(TEMP_MATRIX);
	TEMP_MATRIX.set(
		mlist[0], mlist[1], mlist[2], mlist[3],
		mlist[4], mlist[5], mlist[6], mlist[7],
		mlist[8], mlist[9], mlist[10], mlist[11],
		mlist[12], mlist[13], mlist[14], mlist[15]
	);
	cube.applyMatrix(TEMP_MATRIX);
	cube.translateX(0.5);
	cube.translateY(0.5);
	cube.translateZ(0.5);
}

function setMatrixByArray(m, a) {
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

function loadModelMatrixList() {
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            var mlist = eval(xmlhttp.responseText);
			TJ_MODEL_MTX_LIST = eval(xmlhttp.responseText);
			if (mlist.length > 0) {
				DEBUG_MSG_WINDOW.innerHTML = xmlhttp.responseText;
				// updateCube(mlist);
				UPDATA_TAG = 5;
			} else {
				if (UPDATA_TAG > 0) UPDATA_TAG--;
            }
        }
    };
    CVT_CANVAS.getContext('2d').drawImage(BG_VIDEO, 0, 0, CVT_CANVAS.width, CVT_CANVAS.height);
    xmlhttp.open('POST', '/upload', true);
    xmlhttp.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded;charset=UTF-8');
    xmlhttp.send('b64Frame='+btoa(CVT_CANVAS.toDataURL()));
	// draw();
}

function play() {
	if (SETUP_STATUS == 0) {
		setup();
		SETUP_STATUS = 1;
	}
	BG_VIDEO.play();
    // window.PROC_ID = setInterval(loadModelMatrixList, 50);
}

function detect() {
	loadModelMatrixList();
}

function stop() {
	BG_VIDEO.pause();
    if (window.PROC_ID != null) {
        clearInterval(window.PROC_ID);
        window.PROC_ID = null;
    }
    // window.location.href = '/';
}
