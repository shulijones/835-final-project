from cmath import inf
import cv2
import numpy as np
import random
img = cv2.imread("pics/7.png", -1)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

ret,thresh_img = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)
thresh_img = cv2.dilate(thresh_img, np.ones((45, 45), np.uint8)) 
thresh_img = cv2.medianBlur(thresh_img, 25)

contours, hierarchy = cv2.findContours(thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
contours = sorted(contours, key=cv2.contourArea)
for i in range(len(contours)):
  x,y,w,h = cv2.boundingRect(contours[i])
  print(w, h, w*h)
print(thresh_img.shape)

x,y,w,h = cv2.boundingRect(contours[-2])
#cropped_image = img[y-60:y+h+60,x-60:x+w+60]
cropped_image = img[y:y+h,x:x+w]

colors = [(0, 255, 0), (255, 0, 0), (0, 0, 255), (255, 0, 255), (0, 255, 255), (255, 255, 0), (255, 255, 255)]
for i in range(len(contours)):
  if i == len(contours) - 2:
    color = (0,0,0) # the one we are looking for will always be black
  elif i < len(colors) - 1:
    color = colors[i]
  else:
    color = (random.randrange(0,256), random.randrange(0,256), random.randrange(0,256))
  cv2.drawContours(img, [contours[i]], -1, color, 3)

cv2.namedWindow('main', cv2.WINDOW_KEEPRATIO)
cv2.imshow("main", cropped_image)
cv2.waitKey(0)
