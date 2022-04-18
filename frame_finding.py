from cmath import inf
import cv2
import numpy as np
img = cv2.imread("held_to_wall.jpg", -1)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

ret,thresh_img = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)
thresh_img = cv2.dilate(thresh_img, np.ones((45, 45), np.uint8)) 
thresh_img = cv2.medianBlur(thresh_img, 25)

contours, hierarchy = cv2.findContours(thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
contours = sorted(contours, key=cv2.contourArea)

x,y,w,h = cv2.boundingRect(contours[-3])
cropped_image = img[y:y+h,x :x+w]
cv2.namedWindow('main', cv2.WINDOW_KEEPRATIO)
cv2.imshow("main", cropped_image)
cv2.waitKey(0)
