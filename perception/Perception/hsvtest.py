import numpy as np
import cv2

#cap = cv2.VideoCapture("Formula Student Spain 2015 Endurance- DHBW Engineering with the eSleek15.mp4")
cap = cv2.VideoCapture("Fluela video.mp4")

i = 0
while True:
    i +=1
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #find blue things
    lower_blue = np.array([170/2,30,175])
    upper_blue = np.array([280/2, 255,255])
    mask_blue = cv2.inRange(gray, lower_blue, upper_blue)
    res_blue = cv2.bitwise_and(frame,frame, mask= mask_blue)

    #find yellow things
    lower_yellow = np.array([40 /2,  25, 175])
    upper_yellow = np.array([65 /2, 255,255])
    mask_yellow = cv2.inRange(gray, lower_yellow, upper_yellow)
    res_yellow = cv2.bitwise_and(frame,frame, mask= mask_yellow)

    bit_or = cv2.bitwise_or(mask_blue, mask_yellow)
    res = cv2.bitwise_and(frame, frame, mask= bit_or)

    filter_median = cv2.GaussianBlur(res,(15,15),0) 
    filter_gauss  = cv2.medianBlur(res,15)
    filter_bil    = cv2.bilateralFilter(res,15,75,75)
    #cv2.imshow("frame", frame)
    #cv2.imshow("gray", mask_yellow)
    #cv2.imshow("colorblue", res_blue)
    #cv2.imshow("coloryellow", res_yellow)
    cv2.imshow("color", res)
    cv2.imshow("filter median", filter_median)
    cv2.imshow("filter gausss", filter_gauss)
    cv2.imshow("filter_bil",    filter_bil)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()