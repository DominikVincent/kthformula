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
    print(contours)
    print(hierachie)
    return contours, hierachie

def draw_contours(frame, contours):
    for cnt in contours:
        cv2.drawContours(frame, contours,0,(0,255,0),2)
    
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

    l_h = cv2.getTrackbarPos("LH", "Tracking")
    l_s = cv2.getTrackbarPos("LS", "Tracking")
    l_v = cv2.getTrackbarPos("LV", "Tracking")

    u_h = cv2.getTrackbarPos("UH", "Tracking")
    u_s = cv2.getTrackbarPos("US", "Tracking")
    u_v = cv2.getTrackbarPos("UV", "Tracking")

    i = cv2.getTrackbarPos("continue?", "Tracking")

    lower_blue = np.array([ l_h/2, l_s *2.55, l_v*2.55])
    upper_blue = np.array([ u_h/2, u_s *2.55, u_v*2.55])



    if i == 1:
        ret, frame = cap.read()
        if not ret:
            cap.release()
            cv2.destroyAllWindows()
            exit()
            
    #i +=1
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #find blue things
    #lower_blue = np.array([140 /2, 10  *2.55, 40 *2.55])
    #upper_blue = np.array([260 /2, 100 *2.55, 100 *2,55])
    #lower_blue = np.array([200 /2, 30  *2.55, 15 *2.55])
    #upper_blue = np.array([260 /2, 100 *2.55, 100 *2,55])
    mask_blue = cv2.inRange(gray, lower_blue, upper_blue)
    res_blue = cv2.bitwise_and(frame,frame, mask= mask_blue)

    #find yellow things
    lower_yellow = np.array([40 /2,  40 *2.55, 36*2.55])
    upper_yellow = np.array([65 /2, 100*2.55,100*2.55])
    mask_yellow = cv2.inRange(gray, lower_yellow, upper_yellow)
    res_yellow = cv2.bitwise_and(frame,frame, mask= mask_yellow)
    bit_or = cv2.bitwise_or(mask_blue, mask_yellow)
    res = cv2.bitwise_and(frame, frame, mask= bit_or)

    cont, hier = get_contours(mask_yellow)
    draw_contours(frame, cont)
    draw_contours(mask_yellow, cont)

    #filter_median = cv2.GaussianBlur(res,(15,15),0) 
    #filter_gauss  = cv2.medianBlur(res,15)
    #filter_bil    = cv2.bilateralFilter(res,15,75,75)
    
    
    frame = cv2.resize(frame, (720,480))
    res = cv2.resize(res, (960,540))
    #filter_median = cv2.resize(filter_median, (960,540))
    #filter_gauss = cv2.resize(filter_gauss, (960,540))
    #filter_bil = cv2.resize(filter_bil, (960,540))
    res_blue = cv2.resize(res_blue, (720, 480))
    #res_yellow = cv2.resize(res_yellow, (720,480))
    
    cv2.imshow("frame", frame)
    #cv2.imshow("color", res)
    #cv2.imshow("filter median", filter_median)
    #cv2.imshow("filter gausss", filter_gauss)
    #cv2.imshow("filter_bil",    filter_bil)
    cv2.imshow("gray", mask_yellow)
    #cv2.imshow("colorblue", res_blue)
    #cv2.imshow("coloryellow", res_yellow)
    
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
