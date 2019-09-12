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


    kernel = np.ones((10,5), np.uint8)
    """erosion = cv2.erode(bit_or, kernel, iterations=1)
    dilation = cv2.dilate(bit_or, kernel, iterations=1)
    """
    opening = cv2.morphologyEx(bit_or, cv2.MORPH_OPEN, kernel)
    closeing = cv2.morphologyEx(bit_or, cv2.MORPH_CLOSE, kernel)
    


    #filter_median = cv2.GaussianBlur(res,(15,15),0) 
    #filter_gauss  = cv2.medianBlur(res,15)
    #filter_bil    = cv2.bilateralFilter(res,15,75,75)
    
    bit_or = cv2.resize(bit_or, (960, 540))
    frame = cv2.resize(frame, (960,540))
    res = cv2.resize(res, (960,540))
    #filter_median = cv2.resize(filter_median, (960,540))
    #filter_gauss = cv2.resize(filter_gauss, (960,540))
    #filter_bil = cv2.resize(filter_bil, (960,540))
    res_blue = cv2.resize(res_blue, (960, 540))
    res_yellow = cv2.resize(res_yellow, (960,540))
    opening = cv2.resize(opening, (960, 540))
    closeing = cv2.resize(closeing, (960,540))
    example = frame[346:400, 602:644]
    a = cv2.imwrite("match.png", example)
    cv2.imshow("frame", frame)
    cv2.imshow("mask", bit_or)
    #cv2.imshow("color", res)
    #cv2.imshow("filter median", filter_median)
    #cv2.imshow("filter gausss", filter_gauss)
    #cv2.imshow("filter_bil",    filter_bil)
    #cv2.imshow("gray", mask_yellow)
    #cv2.imshow("colorblue", res_blue)
    #cv2.imshow("coloryellow", res_yellow)
    cv2.imshow("opening", opening)
    cv2.imshow("closeing", closeing)
    
    if i>= 200:
        pass
        #time.sleep(2)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.waitKey(0)
cap.release()
cv2.destroyAllWindows()
