from flask import Flask, render_template, request, jsonify
import base64, hashlib
import numpy as np
import cv2

webAR = Flask(__name__)

webAR.args = dict(
    left = 0,
    top = 50,
    width = 640,
    height = 480,
    test = '[1,2,3,4,5]',
)

@webAR.route('/')
def index():
    return render_template('index.html',
        rand_num= webAR.config['DEBUG'] and np.random.randint(0,1000000),
        args=webAR.args,
    )

@webAR.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        b64 = request.form['b64Frame'].encode()
        cvt = base64.b64decode(b64)
        arr = np.frombuffer(base64.b64decode(cvt[22:]), np.uint8)
        frame = cv2.resize(cv2.imdecode(arr, 0), (640, 480))
        markers = webAR.markerDetector.detect(frame)
        markers_mv = []
        for marker in markers:
            markers_mv.append({'id': marker.marker_id, 'mv': marker.cvt2TJModelView()})
        return jsonify(markers_mv)

if __name__ == '__main__': webAR.run(port=8080, debug=True)
