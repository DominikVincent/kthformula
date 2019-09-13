import numpy as np
import cv2
import time
class cone_detection:
    """
    video_name - name of the video that should be played
    width - width of the window to open, if not changed default is used
    height - height of the window to open, if not change default is used
    driving - activates motiondetection and improves detection
    """
    def __init__(self, video_name, width = -1, height = -1, driving = True):
        self.backgroundSubtractor = cv2.createBackgroundSubtractorMOG2(history = 50, varThreshold=32, detectShadows=True)
        self.cap = cv2.VideoCapture(video_name)
        self.width = width
        self.height = height
        self.driving = driving
        self.run()
        

    """
    gets a frame and removes the stillstanding objects, just keeps motionful objects
    returns:
        frame - input frame just with the motion
        fgmask - bitmask used to keep motion
    """
    def get_motion(self, frame):
        fgmask = self.backgroundSubtractor.apply(frame)
        return cv2.bitwise_and(frame, frame, mask = fgmask), fgmask

    """
    gets a new frame from cap and returns it. if the video is over it destroys all windows and exit()
    return:
        frame in bgr
    """
    def get_new_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            self.cap.release()
            cv2.destroyAllWindows()
            exit()
        return frame

    """
    generates a bitmask which just shows yellow
    return:
        bitmask
    """
    def get_bitmask_yellow(self, frame):
        lower_yellow = np.array([40 /2,  40 *2.55, 36*2.55])
        upper_yellow = np.array([65 /2, 100*2.55,100*2.55])
        mask_yellow = cv2.inRange(frame, lower_yellow, upper_yellow)
        return mask_yellow

    def get_bitmask_blue(self, frame):
        lower_blue = np.array([210 /2, 30  *2.55, 20 *2.55])
        upper_blue = np.array([260 /2, 100 *2.55, 100 *2,55])
        mask_blue = cv2.inRange(frame, lower_blue, upper_blue)
        return mask_blue
    
    def get_bitmask_orange(self, frame):
        lower_orange = np.array([340 /2, 37  *2.55, 60 *2.55])
        upper_orange = np.array([360 /2, 100 *2.55, 100 *2,55])
        mask_orange = cv2.inRange(frame, lower_orange, upper_orange)
        lower_orange = np.array([0 /2, 50  *2.55, 60 *2.55])
        upper_orange = np.array([12 /2, 100 *2.55, 100 *2,55])
        mask_orange2 = cv2.inRange(frame, lower_orange, upper_orange)
        return cv2.bitwise_or(mask_orange, mask_orange2)
    """
    applys cv2.opening with given parameters
    returns modified bitmask
    """
    def apply_opening(self, frame, width= 5, height=5):
        kernel = np.ones((height,width), np.uint8)
        opening = cv2.morphologyEx(frame, cv2.MORPH_OPEN, kernel)
        return opening

    def apply_errosion(slef, frame, width = 5, height = 5, iterations = 1):
        kernel = np.ones((height, width), np.uint8)
        dilation = cv2.erode(frame, kernel, iterations = iterations)
        return dilation

    def apply_dilation(self, frame, width = 5, height = 5, iterations = 1):
        kernel = np.ones((height, width), np.uint8)
        dilation = cv2.dilate(frame, kernel, iterations = iterations)
        return dilation
        
    """
    d – Diameter of each pixel neighborhood that is used during filtering. If it is non-positive, it is computed from sigmaSpace .
    sigmaColor – Filter sigma in the color space. A larger value of the parameter means that farther colors within the pixel neighborhood (see sigmaSpace ) will be mixed together, resulting in larger areas of semi-equal color.
    sigmaSpace – Filter sigma in the coordinate space. A larger value of the parameter means that farther pixels will influence each other as long as their colors are close enough (see sigmaColor ). When d>0 , it specifies the neighborhood size regardless of sigmaSpace . Otherwise, d is proportional to sigmaSpace .
    """
    def apply_bilateral_filter(self, frame, d=15, sigmaC=75, sigmaS=75):
        return cv2.bilateralFilter(res,d,sigmaC,sigmaS)

    def get_contours(self, frame):
        contours, hierachie = cv2.findContours(frame, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)
        return contours, hierachie

    def draw_contours(self, frame, contours, min_size=0, max_size=10000000):
        print("\n")
        for cnt in contours:
            #print(cv2.contourArea(cnt))
            #print("min_size: ", min_size, " max_size: ", max_size)
            if  min_size < cv2.contourArea(cnt) < max_size:
                x,y,w,h = cv2.boundingRect(cnt)
                frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
                continue
            #print("not drawn with", cv2.contourArea(cnt))

    def run(self):
        while True:
            frame = self.get_new_frame()
            x = frame.shape[1]
            y = frame.shape[0]
            
            
            if(self.driving):
                frame_motion, mask = self.get_motion(frame)
            else:
                frame_motion = frame

            frame_hsv = cv2.cvtColor(frame_motion, cv2.COLOR_BGR2HSV)

            mask_yellow = self.get_bitmask_yellow(frame_hsv)
            mask_blue   = self.get_bitmask_blue(frame_hsv)
            mask_orange = self.get_bitmask_orange(frame_hsv)
            mask_combined = cv2.bitwise_or(mask_blue, mask_yellow)
            mask_combined = cv2.bitwise_or(mask_combined, mask_orange)

            
            
            x_opening =  int(x / 280)
            y_opening = int(y/160)
            mask_combined = self.apply_opening(mask_combined, x_opening, y_opening)
            mask_combined = self.apply_errosion(mask_combined, x_opening, y_opening, iterations = 3)
            
            x_dilation = int(x/100)
            y_dilation = int(y/40)
            mask_combined = self.apply_dilation(mask_combined,x_dilation, y_dilation, 3)




            cont, hier = self.get_contours(mask_combined)
            
            #frame = cv2.bitwise_and(frame, frame, mask=mask_combined)
            size_max = x*y/150 * 4 - 3*x*y/150*self.driving
            size_min = x*y/2724
            self.draw_contours(frame, cont, size_min, size_max)

            if (self.width != -1):
                mask_combined = cv2.resize(mask_combined, (self.width, y))
                frame = cv2.resize(frame, (self.width, y))
                x = self.width

            if (self.height != -1):
                mask_combined = cv2.resize(mask_combined, (x, self.height))
                frame = cv2.resize(frame, (x, self.height))
            cv2.imshow("mask", mask_combined)
            cv2.imshow("motion", frame)
            

            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.cap.release()
                cv2.destroyAllWindows()

            #time.sleep(0.1)

if __name__== "__main__":
    #cone_detection("video_long.mp4", driving = True, width = 1280 , height = 720).run()
    #cone_detection("video.mp4", driving = True, width = 1280 , height = 720).run()
    cone_detection("video_hdr.mp4", driving = False, width = 1280 , height = 720).run()
    #cone_detection("video_indoor.mp4", driving = False, width = 1280 , height = 720).run()
