# USAGE
# import the necessary packages
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
import os
from arcface_fd import FaceDetector
from arcface_fr import FaceRecognition
from arcface_fga import FaceGenderage
from numpy import dot
from numpy.linalg import norm

fd = FaceDetector({'prefix':'./model/rentina-net/model','epoch':0000})
fd.prepare(0)

fr = FaceRecognition({'prefix':'./model/r100-arcface-net/model','epoch':0000})
fr.prepare(0)

fga = FaceGenderage({'prefix':'./model/gender-age-net/model','epoch':0000})
fga.prepare(0)

# initialize the output frame and a lock used to ensure thread-safe
# exchanges of the output frames (useful for multiple browsers/tabs
# are viewing tthe stream)
outputFrame = None
lock = threading.Lock()

# construct the argument parser and parse command line arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i","--id", type=str,required=True,
	help="ID")
ap.add_argument("-u","--url", type=str,required=True,
	help="url")
ap.add_argument("-f", "--frame-count", type=int, default=32,
	help="# of frames used to construct the background model")
args = vars(ap.parse_args())

# initialize a flask object
app = Flask(__name__)
# initialize the video stream and allow the camera sensor to
# warmup
#vs = VideoStream(usePiCamera=1).start()
if args['url'] == '0':
	args['url'] = 0
vs = VideoStream(src=args['url']).start()
time.sleep(2.0)

@app.route("/"+args['id'])
def index():
	# return the rendered template
	return render_template("index.html")

base = []
label = []

def train_data(path):
    img_names = os.listdir(path)

    for img_name in img_names:
        image = cv2.imread(path+img_name)

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image,(640,480))
        #image = imutils.resize(image, width=480)
        results, lm  = fd.detect(image)
        
        # loop over the detections
        for dets in results:
            startX = int(dets[0])
            startY = int(dets[1])
            endX = int(dets[2])
            endY = int(dets[3])
            scores = dets[4]

            if scores > 0.9:
                emd = fr.get_embedding(image[startY:endY,startX:endX])[0]
                base.append(emd)
                label.append(img_name.split('.')[0])

print('train data.....')
train_data('./known_people/')
print('Done')
print(label)

def recognition (face):
	ebd = fr.get_embedding(face)[0]
	confi = 0.5
	result = 'Unknown'
	for i,emd in enumerate(base):
		cos_sim = dot(ebd, emd)/(norm(ebd)*norm(emd))#fr.compute_sim(ebd,emd)
		if cos_sim > confi:
			confi = cos_sim
			result = "{:.2f}%".format(confi * 100) +' '+ label[i]
	return result

def face_recognition(frameCount):
	# grab global references to the video stream, output frame, and
	# lock variables
	global vs, outputFrame, lock

	total = 0

	# loop over frames from the video stream
	while True:
		# read the next frame from the video stream, resize it,
		# convert the frame to grayscale, and blur it
		frame = vs.read()
		frame = imutils.resize(frame, width=1280)
		image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

		results, lm  = fd.detect(image)
		# loop over the detections
		for dets in results:
			startX = int(dets[0])
			startY = int(dets[1])
			endX = int(dets[2])
			endY = int(dets[3])
			scores = dets[4]

			if scores > 0.9:
				if startX < 0 or startY <0:
					continue
					
				face = image[startY:endY, startX:endX]
				rs = recognition(face)
				gender, age = fga.get(face)

				# draw the bounding box of the face along with the associated
				# probability
				name = 'Name: '+ rs
				gen = "Gender: " + str(gender)
				ag = "Age: " + str(age)

                # if rs != '':
                #     cv2.imwrite(save_face+text+'.jpg', cv2.cvtColor(face, cv2.COLOR_RGB2BGR))
			
				#Draw face into frame
				cv2.rectangle(frame, (startX, startY), (endX,endY), (0, 0, 255), 2)
				cv2.rectangle(frame, (startX, endY + 50), (endX, endY), (0, 0, 255), cv2.FILLED)
				font = cv2.FONT_HERSHEY_DUPLEX
				cv2.putText(frame, name, (startX + 6, endY + 15), font ,0.45, (255, 255, 255), 1)
				cv2.putText(frame, gen, (startX + 6, endY + 30), font,0.45 ,(255, 255, 255), 1)
				cv2.putText(frame, ag, (startX + 6, endY + 45), font, 0.45,(255, 255, 255), 1)

		# grab the current timestamp and draw it on the frame
		timestamp = datetime.datetime.now()

		cv2.putText(frame, timestamp.strftime(
			"%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),
			cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

		with lock:
			outputFrame = frame.copy()

def detect_motion(frameCount):
	# grab global references to the video stream, output frame, and
	# lock variables
	global vs, outputFrame, lock

	total = 0

	# loop over frames from the video stream
	while True:
		# read the next frame from the video stream, resize it,
		# convert the frame to grayscale, and blur it
		frame = vs.read()
		#frame = imutils.resize(frame, width=400)
		
		# grab the current timestamp and draw it on the frame
		timestamp = datetime.datetime.now()
		cv2.putText(frame, timestamp.strftime(
			"%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),
			cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

		with lock:
			outputFrame = frame.copy()
		
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
	# start a thread that will perform motion detection
	t = threading.Thread(target=face_recognition, args=(
		args["frame_count"],))
	t.daemon = True
	t.start()

	# start the flask app
	app.run(host="0.0.0.0", port="8001", debug=True,
		threaded=True, use_reloader=False)

# release the video stream pointer
vs.stop()	