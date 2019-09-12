import numpy as np
import cv2
import time

#cap = cv2.VideoCapture("Formula Student Spain 2015 Endurance- DHBW Engineering with the eSleek15.mp4")
cap = cv2.VideoCapture("video_long.mp4")

i = 0
while True:
    i +=1
    ret, frame = cap.read()
    if not ret:
        cap.release()
        cv2.destroyAllWindows()
        exit()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #find blue things
    #lower_blue = np.array([140 /2, 10  *2.55, 40 *2.55])
    #upper_blue = np.array([260 /2, 100 *2.55, 100 *2,55])
    lower_blue = np.array([200 /2, 30  *2.55, 15 *2.55])
    upper_blue = np.array([250 /2, 100 *2.55, 100 *2,55])
    mask_blue = cv2.inRange(gray, lower_blue, upper_blue)
    res_blue = cv2.bitwise_and(frame,frame, mask= mask_blue)

    #find yellow things
    lower_yellow = np.array([40 /2,  40 *2.55, 36*2.55])
    upper_yellow = np.array([65 /2, 100*2.55,100*2.55])
    mask_yellow = cv2.inRange(gray, lower_yellow, upper_yellow)
    res_yellow = cv2.bitwise_and(frame,frame, mask= mask_yellow)

    bit_or = cv2.bitwise_or(mask_blue, mask_yellow)
    res = cv2.bitwise_and(frame, frame, mask= bit_or)

    #filter_median = cv2.GaussianBlur(res,(15,15),0) 
    #filter_gauss  = cv2.medianBlur(res,15)
    #filter_bil    = cv2.bilateralFilter(res,15,75,75)
    
    
    frame = cv2.resize(frame, (960,540))
    res = cv2.resize(res, (960,540))
    #filter_median = cv2.resize(filter_median, (960,540))
    #filter_gauss = cv2.resize(filter_gauss, (960,540))
    #filter_bil = cv2.resize(filter_bil, (960,540))
    res_blue = cv2.resize(res_blue, (960, 540))
    res_yellow = cv2.resize(res_yellow, (960,540))
    
    cv2.imshow("frame", frame)
    #cv2.imshow("color", res)
    #cv2.imshow("filter median", filter_median)
    #cv2.imshow("filter gausss", filter_gauss)
    #cv2.imshow("filter_bil",    filter_bil)
    #cv2.imshow("gray", mask_yellow)
    cv2.imshow("colorblue", res_blue)
    cv2.imshow("coloryellow", res_yellow)
    
    if i>= 200:
        pass
        #time.sleep(2)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
