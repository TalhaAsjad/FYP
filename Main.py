import cv2
import numpy as np
import sys
import statistics
import time

# Reading Video
cap = cv2.VideoCapture('1.mp4')

# Background Subtraction
mask = cv2.createBackgroundSubtractorMOG2(history=1, varThreshold=15, detectShadows=False)
# Making matrix for Erosion, dilation and morphing
kernel = np.ones((2, 2), np.uint8)
kernel1 = np.ones((1, 2), np.uint8)

# (major_ver, minor_ver, subminor_ver) = (cv2._version_).split('.')
# if int(major_ver) < 3:
fps = cap.get(cv2.CAP_PROP_FPS)
print("FPS: {0}".format(fps))
# else:
#     fps = cap.get(cv2.CAP_PROP_FPS)
#     print("FPS: {0}".format(fps))

# Global Variables
leftwidth = []
rightwidth = []
leftheight = []
rightheight = []


while cap.isOpened():

    ret, frame = cap.read()
    if not ret:
        break
    frame1 = frame

    a, b, c = frame.shape

    mask1 = mask.apply(frame)
    # Erosion
    mask1 = cv2.erode(mask1, kernel, iterations=1)
    # Dialtion
    mask1 = cv2.dilate(mask1, kernel1, iterations=3)
    # Morphing
    # mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, kernel)
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(mask1.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for c in contours:
        if cv2.contourArea(c) < 400:
            continue
        elif cv2.contourArea(c) > 1000:
            # print(len(contours))
            (x, y, w, h) = cv2.boundingRect(c)

            if x < b / 2:
                # Using cv2.putText() method
                # frame = cv2.putText(frame, 'Left', org, font, fontScale, color, thickness, cv2.LINE_AA)
                leftwidth.append(w)
                leftheight.append(h)
            elif x > b / 2:
                # frame = cv2.putText(frame, 'Right', org, font, fontScale, color, thickness, cv2.LINE_AA)
                rightwidth.append(w)
                rightheight.append(h)
cap.release()


if b in leftwidth :
     leftwidth.remove(b)
if a in leftheight :
     leftheight.remove(a)

lw = statistics.mode(leftwidth)
lh = statistics.mode(leftheight)

if b in rightwidth :
     rightwidth.remove(b)
if a in rightwidth :
     rightheight.remove(a)

rw = statistics.mode(rightwidth)
rh = statistics.mode(rightheight)

avgw = (lw+rw)/2
avgh = (lh+rh)/2

print(int(avgw),int(avgh))
# t = int(time.time())*1000
print(time.time()*1000)
# Going Through Video again

# Reading Video
cap = cv2.VideoCapture('1.mp4')

# Background Subtraction
mask = cv2.createBackgroundSubtractorMOG2(history=1, varThreshold=15, detectShadows=False)
# Making matrix for Erosion, dilation and morphing
kernel = np.ones((2, 2), np.uint8)
kernel1 = np.ones((1, 2), np.uint8)


while cap.isOpened():

    ret, frame = cap.read()
    if not ret:
        break
    frame1 = frame

    a, b, c = frame.shape
    # print(a,b)

    mask1 = mask.apply(frame)
    # Erosion
    mask1 = cv2.erode(mask1, kernel, iterations=1)
    # Dialtion
    mask1 = cv2.dilate(mask1, kernel1, iterations=15)
    # Morphing
    # mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, kernel)
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(mask1.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for c in contours:
        if cv2.contourArea(c) < 400:
            continue
        elif cv2.contourArea(c) > 1500:
            # print(len(contours))
            (x, y, w, h) = cv2.boundingRect(c)

            # print(cv2.contourArea(c))

            font = cv2.FONT_HERSHEY_SIMPLEX

            # org
            org = (x, y)

            # fontScale
            fontScale = 0.75

            # Blue color in BGR
            color = (255, 255, 100)

            # Line thickness of 2 px
            thickness = 2
            text = str(x) + ", " + str(y)

            if x < b / 2:
                # Using cv2.putText() method
                frame = cv2.putText(frame, 'Left', org, font, fontScale, color, thickness, cv2.LINE_AA)
                w = lw
                h= lh
            elif x > b / 2:
                frame = cv2.putText(frame, 'Right', org, font, fontScale, color, thickness, cv2.LINE_AA)
                w = rw
                h = rh

            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 2)
            # time.sleep(.1)


            upper_left = (x, y)
            bottom_right = (x + w, y + h)
            frame1 = frame[upper_left[1]: bottom_right[1], upper_left[0]: bottom_right[0]]
            roi = frame1

    # cv2.imshow('result', masked_image)
    # cv2.imshow('result', frame)
    cv2.imshow('result', roi)
    k = cv2.waitKey(30) & 0xFF
    if k == 27:
        break
# This is where the video is read

cap.release()
cv2.destroyAllWindows()