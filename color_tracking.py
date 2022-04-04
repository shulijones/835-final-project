#! /usr/bin/env python

import cv2

vid = cv2.VideoCapture(0)


while True:
    ret, img = vid.read()
    # img = cv2.imread("green.jpg", -1)
    #blur the source image to reduce color noise
    img = cv2.GaussianBlur(img,(11,11),0)
    overlay = img
    thresholded_img = img
    #convert the image to hsv(Hue, Saturation, Value) so its
    #easier to determine the color to track(hue)

    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #limit all pixels that don't match our criteria, in this case we are
    #looking for purple but if you want you can adjust the first value in
    #both turples which is the hue range(120,140).  OpenCV uses 0-180 as
    #a hue range for the HSV color model
    thresholded_img = cv2.inRange(hsv_img, (40,55,55), (80,255,255))
    thresholded_img = cv2.erode(thresholded_img, None, iterations=2)
    thresholded_img = cv2.dilate(thresholded_img, None, iterations=2)
    contours, hierarchy = cv2.findContours(thresholded_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if len(contours) != 0:
        big_contour = max(contours, key=cv2.contourArea)
        cv2.drawContours(img, big_contour, -1, (0, 255, 0), 3)
    #determine the objects moments and check that the area is large
    #enough to be our object
    # moments = cv2.moments(thresholded_img)
        moments = cv2.moments(big_contour)
    else:
        moments = cv2.moments(thresholded_img)
    area = moments['m00'] 

    print(area)
    #there can be noise in the video so ignore objects with small areas
    if(area != 0):
        #determine the x and y coordinates of the center of the object
        #we are tracking by dividing the 1, 0 and 0, 1 moments by the area
        x = int(moments['m10']/area)
        y = int(moments['m01']/area)

        #print 'x\: ' + str(x) + ' y\: ' + str(y) + ' area\: ' + str(area)

        #create an overlay to mark the center of the tracked object
        # overlay = cv.CreateImage(cv.GetSize(img), 8, 3)
        overlay = cv2.circle(img, (x, y), 20, (255, 0, 0), 10)

        # overlay = cv2.circle(img, (x, y), 20, (255, 0, 0), 10)
        # cv.Add(img, overlay, img)
        #add the thresholded image back to the img so we can see what was
        #left after it was applied
        # cv2.Merge(thresholded_img, None, None, None, img)

#display the image
    cv2.namedWindow("custom_window", cv2.WINDOW_FREERATIO)
    cv2.imshow("custom_window", img)

    # cv2.imshow("color_tracker_window2", thresholded_img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
# After the loop release the cap object
vid.release()
# # Destroy all the windows
cv2.destroyAllWindows()


