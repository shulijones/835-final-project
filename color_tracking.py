#! /usr/bin/env python

# test file for color tracking code

import cv2

vid = cv2.VideoCapture(0)


while True:
    ret, img = vid.read()
    img = cv2.GaussianBlur(img,(11,11),0)
    overlay = img
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

    print(area)
    if(area != 0):
        #determine the x and y coordinates of the center of the object
        x = int(moments['m10']/area)
        y = int(moments['m01']/area)
        overlay = cv2.circle(img, (x, y), 20, (255, 0, 0), 10)


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


