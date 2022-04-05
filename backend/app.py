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
import numpy as np

outputFrame = None
colorOutputFrame = None

# initialize a flask object
app = Flask(__name__)

# initialize the video stream and allow the camera sensor to warm up
vs = VideoStream(src=0).start() # pulling from webcam
time.sleep(2.0)

@app.route("/") # main page
def index():
	return render_template("index.html")

def get_video(frameCount):
  global vs, outputFrame, colorOutputFrame # vs = video stream
  # loop over frames from the video stream
  while True:
    # read the next frame from the video stream and resize it
    frame = vs.read()
    frame = imutils.resize(frame, width=400)
    flipped_frame = cv2.flip(frame, flipCode=1)
    outputFrame = flipped_frame.copy()


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

def color_track_frame():
    global colorOutputFrame
    img = cv2.GaussianBlur(outputFrame,(11,11),0)
    overlay = outputFrame
    thresholded_img = img
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    thresholded_img = cv2.inRange(hsv_img, (40,55,55), (80,255,255))
    thresholded_img = cv2.erode(thresholded_img, None, iterations=2)
    thresholded_img = cv2.dilate(thresholded_img, None, iterations=2)
    contours, hierarchy = cv2.findContours(thresholded_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if len(contours) != 0:
        big_contour = max(contours, key=cv2.contourArea)
        cv2.drawContours(img, big_contour, -1, (0, 255, 0), 3)
        moments = cv2.moments(big_contour)
    else:
        moments = cv2.moments(thresholded_img)
    area = moments['m00'] 

    if(area != 0):
        #determine the x and y coordinates of the center of the object
        x = int(moments['m10']/area)
        y = int(moments['m01']/area)
        overlay = cv2.circle(outputFrame, (x, y), 20, (255, 0, 0), 10)
    colorOutputFrame = overlay

def generate_color_tracking():
  global colorOutputFrame
	# loop over frames from the output stream
  while True:
    # check if the output frame is available, otherwise skip
    # the iteration of the loop 
    if outputFrame is None:
      continue
    color_track_frame()
    (flag, encodedImage) = cv2.imencode(".jpg", colorOutputFrame)
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


@app.route("/get_picture")
def get_picture():
  # return a single video frame (as jpg)
  global outputFrame
  if outputFrame is not None:
    # crop the image to just show the picture (which we find via contours)
    gray = cv2.cvtColor(outputFrame, cv2.COLOR_BGR2GRAY)

    ret,thresh_img = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)
    thresh_img = cv2.dilate(thresh_img, np.ones((45, 45), np.uint8)) 
    thresh_img = cv2.medianBlur(thresh_img, 25)

    contours, hierarchy = cv2.findContours(thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contours = sorted(contours, key=cv2.contourArea)

    x,y,w,h = cv2.boundingRect(contours[-2])
    cropped_image = outputFrame[y:y+h,x :x+w]

    # encode the image as a jpg and check the encoding was successful
    (flag, encodedImage) = cv2.imencode(".jpg", cropped_image)
    if flag:
		# yield the output frame in base 64 format
      im_bytes = encodedImage.tobytes()
      im_b64 = base64.b64encode(im_bytes)
      return Response(im_b64)
  return "Request error"

@app.route("/video_feed_color")
def video_feed_color():
	# return the response generated along with the specific media
	# type (mime type); this type continuously replaces itself
  # each time the word "frame" appears in the stream

  return Response(generate_color_tracking(),
		mimetype = "multipart/x-mixed-replace; boundary=frame")
   
if __name__ == '__main__':
  # start a thread to get the video stream
	t = threading.Thread(target=get_video, args=(32,)) # frame count 32
	t.daemon = True
	t.start()
	# start the flask app
	app.run(debug=True, threaded=True, use_reloader=False)
# release the video stream pointer
vs.stop()