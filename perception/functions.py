import numpy as np
import cv2

class cone_detection:
    
    def __init__(self):
        self.backgroundSubtractor = cv2.createBackgroundSubtractorMOG2(history = 50, varThreshold=32, detectShadows=True)
        

    """
    gets a frame and removes the stillstanding objects, just keeps motionful objects
    returns:
        frame - input frame just with the motion
        fgmask - bitmask used to keep motion
    """
    def detect_motion(self, frame):
        fgmask = self.backgroundSubtractor.apply(frame)
        return cv2.bitwise_and(frame, frame, mask = fgmask), fgmask
    