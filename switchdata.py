import numpy as np
import cv2
import serial
import time

class SwitchData:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        print(self.cap.set(3,1280))
        print(self.cap.set(4,720))


    def update(self):
        # Capture frame-by-frame
        self.ret, self.frame = self.cap.read()

    def show(self):
        cv2.imshow('frame', self.frame)

    def specialAnalysis(self):
        s = self.frame[507:587, 1051:1235]
        s = cv2.cvtColor(s, cv2.COLOR_BGR2GRAY)
        self.ret, s = cv2.threshold(s, 200, 255, cv2.THRESH_BINARY)
        cv2.imshow('frame', self.frame)
        cv2.imshow('frame', s)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            return False