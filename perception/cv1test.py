import numpy as np
import cv2

#cap = cv2.VideoCapture("Formula Student Spain 2015 Endurance- DHBW Engineering with the eSleek15.mp4")
cap = cv2.VideoCapture("Fluela Video.mp4")

i = 0
while True:
    i +=1
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #height, width = gray.shape
    #cv2.rectangle(gray,(15 + i % width,25), (200 + i % width,150),122,15)
    retval, threshold = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY_INV)
    th = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 101, 0)

    cv2.imshow("grayVideo", frame)
    cv2.imshow('threshold',threshold)
    cv2.imshow('thresholdgauss',th)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()