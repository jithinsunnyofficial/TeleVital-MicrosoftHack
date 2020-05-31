# USAGE
# python webstreaming.py --ip 0.0.0.0 --port 8000

# import the necessary packages
from application.face_recognition import Recog
from imutils.video import VideoStream
from flask import Response
from flask import Flask
from flask import render_template
import threading
import argparse
import datetime
import imutils
import time
import cv2
from tts import convert_and_play
from stt import generate_text
import concurrent.futures
from flow import flow
from playsound import playsound
from dialogflow_api import analyze_text
from keras.models import load_model
from label_detect import classify_face

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
cascadePath = "Cascades/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)
font = cv2.FONT_HERSHEY_SIMPLEX

names = ['Joel', 'Farhan', 'Jithin']
id = 0 #facearray index

# initialize the output frame and a lock used to ensure thread-safe
# exchanges of the output frames (useful for multiple browsers/tabs
# are viewing tthe stream)
outputFrame = None
lock = threading.Lock()

# initialize a flask object
app = Flask(__name__)

# initialize the video stream and allow the camera sensor to
# warmup
#vs = VideoStream(usePiCamera=1).start()
vs = cv2.VideoCapture(0)
vs.set(3, 640) # set video widht
vs.set(4, 480) # set video height
# Define min window size to be recognized as a face
minW = 0.1*vs.get(3)
minH = 0.1*vs.get(4)
time.sleep(2.0)

def apicaller(text, session_id):
	final_text = analyze_text(text session_id)
	if final_text != 'end':
		convert_and_play(final_text)
		apicaller(analyze_text(generate_text), session_id)



def detect_face(frameCount):
	# grab global references to the video stream, output frame, and
	# lock variables
	global vs, outputFrame, lock

	# initialize the motion detector and the total number of frames
	# read thus far
	md = Recog(accumWeight=0.1)
	total = 0

	# loop over frames from the video stream
	frame_counter = 0 
	face_frame_counter = 0
	previous_state = 0
	previous_id = 'unknown'
	counter_id = 0
	flag = False
	mainFlag = False
	flagTemp = 0
	finalFlag = True
	while True:
		ret, frame = vs.read()
		try:
			x = th.is_alive()
			if x == False and flagTemp == 0:
				flagTemp = 1
				frame_counter = 0 
				face_frame_counter = 0
				previous_state = 0
				previous_id = 'unknown'
				counter_id = 0
				flag = False
				mainFlag = False
		except:
			pass
		if finalFlag:

			# read the next frame from the video stream, resize it,
			# convert the frame to grayscale, and blur it
			
			frame_counter+=1
			
			msg = ""
			#frame = imutils.resize(frame, width=400)
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			gray = cv2.GaussianBlur(gray, (7, 7), 0)

			# grab the current timestamp and draw it on the frame
			timestamp = datetime.datetime.now()
			cv2.putText(frame, timestamp.strftime(
				"%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),
				cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

			# if the total number of frames has reached a sufficient
			# number to construct a reasonable background model, then
			# continue to process the frame
			if total > frameCount:
				# detect motion in the image
				faces = faceCascade.detectMultiScale(
					gray,
					scaleFactor=1.2,
					minNeighbors=5,
					minSize=(int(minW), int(minH)),
				)
				
				
				#print(faces)
				if len(faces)>0:
					# print("face detected")
					if previous_state == 1:
						face_frame_counter+=1
					
					previous_state = 1
				else:
					previous_state = 0
					face_frame_counter = 0
				

				if face_frame_counter>70:
					#start seq.
					print('face recognized')
					for(x,y,w,h) in faces:
						cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
						id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
						if counter_id>10:
							
							print(previous_id)
							tempstr = 'Hello '+names[id]
							finalFlag = False
							mainFlag = True
							flagTemp = 0
							a = 0
							th = threading.Thread(target = flow, args= (names[id],))
							th.start()
							#print(th.is_alive())
						
							flag = True
						
						if(confidence<100):
							
							id = names[id]
							if (id==previous_id):
								counter_id+=1
							previous_id = id
						else: 
							id = 'unknown'
							previous_id = id
							counter_id = 0
					
					#face_frame_counter = 0
				
			total += 1

			# acquire the lock, set the output frame, and release the
			# lock
		with lock:
			outputFrame = frame.copy()



@app.route("/")
def index():
	t = threading.Thread(target=detect_face, args=(
		args["frame_count"],))
	t.daemon = True
	t.start()
	# return the rendered template
	return render_template("index.html")


		
def generate():
	# grab global references to the output frame and lock variables
	global outputFrame, lock

	# loop over frames from the output stream
	while True:
		# wait until the lock is acquired
		with lock:
			# check if the output frame is available, otherwise skip
			# the iteration of the loop
			if outputFrame is None:
				continue

			# encode the frame in JPEG format
			(flag, encodedImage) = cv2.imencode(".jpg", outputFrame)

			# ensure the frame was successfully encoded
			if not flag:
				continue

		# yield the output frame in the byte format
		yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
			bytearray(encodedImage) + b'\r\n')

@app.route("/video_feed")
def video_feed():
	# return the response generated along with the specific media
	# type (mime type)
	return Response(generate(),
		mimetype = "multipart/x-mixed-replace; boundary=frame")

# check to see if this is the main thread of execution
if __name__ == '__main__':
	# construct the argument parser and parse command line arguments
	ap = argparse.ArgumentParser()
	ap.add_argument("-i", "--ip", type=str, default='127.0.0.1',
		help="ip address of the device")
	ap.add_argument("-o", "--port", type=int, default=8000,
		help="ephemeral port number of the server (1024 to 65535)")
	ap.add_argument("-f", "--frame-count", type=int, default=32,
		help="# of frames used to construct the background model")
	args = vars(ap.parse_args())

	# start a thread that will perform motion detection

	# start the flask app
	app.run(host=args["ip"], port=args["port"], debug=True,
		threaded=True, use_reloader=False)

# release the video stream pointer
vs.release
