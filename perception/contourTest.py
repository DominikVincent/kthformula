import numpy as np
import cv2
import time


def nothing(x):
    pass

def change_i(x):
    i = x
    return

def get_contours(frame):
    contours, hierachie = cv2.findContours(frame, mode=cv2.RETR_LIST, method=cv2.CHAIN_APPROX_SIMPLE)

    return contours, hierachie

def draw_contours(frame, contours):
    for cnt in contours:
        if  50 < cv2.contourArea(cnt) < 5000:
            cv2.drawContours(frame, [cnt],0,(0,255,0),2)
            
    
#cap = cv2.VideoCapture("Formula Student Spain 2015 Endurance- DHBW Engineering with the eSleek15.mp4")
cap = cv2.VideoCapture("video.mp4")
sliders = cv2.namedWindow("Tracking")

cv2.createTrackbar("LH", "Tracking", 0,   360, nothing)
cv2.createTrackbar("LS", "Tracking", 0,   100, nothing)
cv2.createTrackbar("LV", "Tracking", 0,   100, nothing)
cv2.createTrackbar("UH", "Tracking", 360, 360, nothing)
cv2.createTrackbar("US", "Tracking", 100, 100, nothing)
cv2.createTrackbar("UV", "Tracking", 100, 100, nothing)
cv2.createTrackbar("continue?", "Tracking", 1, 1, nothing)
i = 1
while True:
    i = cv2.getTrackbarPos("continue?", "Tracking")
    if i == 1:
        ret, frame = cap.read()
        if not ret:
            cap.release()
            cv2.destroyAllWindows()
            exit()
    
        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        #find yellow things
        lower_yellow = np.array([40 /2,  40 *2.55, 36*2.55])
        upper_yellow = np.array([65 /2, 100*2.55,100*2.55])
        mask_yellow = cv2.inRange(frame_hsv, lower_yellow, upper_yellow)
        res_yellow = cv2.bitwise_and(frame,frame, mask= mask_yellow)
        
    cont, hier = get_contours(mask_yellow)
    print("\n\n",len(cont))
    draw_contours(frame, cont)
    draw_contours(mask_yellow, cont)

   
   
    cv2.imshow("frame", frame)
    
    cv2.imshow("mask", mask_yellow)
    
    
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
