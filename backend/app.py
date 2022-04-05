# code skeleton heavily based on tutorial: 
# https://pyimagesearch.com/2019/09/02/opencv-stream-video-to-web-browser-html-page/

# import the necessary packages
from imutils.video import VideoStream
from flask import Response
from flask import Flask
from flask import render_template
import threading
import imutils
import time
import cv2
import base64

outputFrame = None

# initialize a flask object
app = Flask(__name__)

# initialize the video stream and allow the camera sensor to warm up
vs = VideoStream(src=0).start() # pulling from webcam
time.sleep(2.0)

@app.route("/") # main page
def index():
	return render_template("index.html")

def get_video(frameCount):
  global vs, outputFrame # vs = video stream
  # loop over frames from the video stream
  while True:
    # read the next frame from the video stream and resize it
    frame = vs.read()
    frame = imutils.resize(frame, width=400)
    outputFrame = frame.copy()

def generate():
  global outputFrame
	# loop over frames from the output stream
  while True:
    # check if the output frame is available, otherwise skip
    # the iteration of the loop
    if outputFrame is None:
      continue
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
	# type (mime type); this type continuously replaces itself
  # each time the word "frame" appears in the stream
  return Response(generate(),
		mimetype = "multipart/x-mixed-replace; boundary=frame")

@app.route("/current_image")
def current_image():
  # return a single video frame (as jpg)
  global outputFrame
  if outputFrame is not None:
    (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)
    # ensure the frame was successfully encoded
    if flag:
		# yield the output frame in base 64 format
      im_bytes = encodedImage.tobytes()
      im_b64 = base64.b64encode(im_bytes)
      return Response(im_b64)
  return "Request error"
   
if __name__ == '__main__':
  # start a thread to get the video stream
	t = threading.Thread(target=get_video, args=(32,)) # frame count 32
	t.daemon = True
	t.start()
	# start the flask app
	app.run(debug=True, threaded=True, use_reloader=False)
# release the video stream pointer
vs.stop()