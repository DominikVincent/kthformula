import numpy as np
import cv2
import time

#cap = cv2.VideoCapture("Formula Student Spain 2015 Endurance- DHBW Engineering with the eSleek15.mp4")
cap = cv2.VideoCapture("video_hdr.mp4")

i = 1

while i==1:
    i +=1
    ret, frame = cap.read()

    template = cv2.imread('match.png',0)
    w, h = template.shape[::-1]

    if not ret:
        cap.release()
        cv2.destroyAllWindows()
        exit()
   
    
    
    frame = cv2.resize(frame, (960,540))
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    res = cv2.matchTemplate(gray_frame,template,cv2.TM_CCOEFF_NORMED)
    threshold = 0.6
    loc = np.where( res >= threshold)

    for pt in zip(*loc[::-1]):
        cv2.rectangle(frame, pt, (pt[0] + w, pt[1] + h), (0,255,255), 2)

    cv2.imshow("frame", frame)
    
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.waitKey(0)
cap.release()
cv2.destroyAllWindows()
