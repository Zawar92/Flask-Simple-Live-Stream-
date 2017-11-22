from flask import Flask,render_template, Response
from PIL import Image, ImageFont, ImageDraw
from imutils.object_detection import non_max_suppression
from imutils import paths
import dlib
import imutils
from imutils import face_utils
import numpy as np
import cv2
import io
app = Flask(__name__)

# To route to Index template folder
@app.route('/')
def index():
    return render_template('index.html')

#Get frames from An RTSP stream To get Frontal Faces
def gen():
	cam = "Your Rtsp stream"
	cap = cv2.VideoCapture(cam)
	#body_cascade = cv2.CascadeClassifier('static/haarcascade_frontalface_default.xml')
	detector = dlib.get_frontal_face_detector()
	stack=list()
	while True:
		ret, frame = cap.read()
		print frame
		frame=np.array(frame)
		frame = imutils.resize(frame, width=400)
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		#body = body_cascade.detectMultiScale(frame, 1.3, 5)
		dets = detector(gray, 1)
		for k, d in enumerate(dets):
			cv2.rectangle(frame,(d.left(),d.top()),(d.right(),d.bottom()),(255,0,0),2)



		#for (x,y,w,h) in body:
		#	cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
		ret, jpeg = cv2.imencode('.jpg', frame)
		#convjpg = Image.fromarray(frame)
		#cv2.imshow(frame)
		#imgByteArr=io.BytesIO()
		#convjpg.save(imgByteArr,format="jpeg")
		#imgByteArr=imgByteArr.getvalue()
		yield (b'--frame\r\n'b'Content-Type: image/png\r\n\r\n' + jpeg.tobytes() + b'\r\n')

		
	cap.release()
	cv2.destroyAllWindows()


@app.route('/livestream')
def livestream():
	return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run()

