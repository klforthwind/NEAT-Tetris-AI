import numpy as np
import cv2
import serial
import time

class SwitchData:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        print(self.cap.set(3,1280))

    def update(self):
        # Capture frame-by-frame
		self.ret, self.frame = cap.read()
        
    def show(self):
        cv2.imshow('frame', self.frame)

    def specialAnalysis(self):
        self.s = self.frame[507:587, 1051:1235]
		self.s = cv2.cvtColor(self.s, cv2.COLOR_BGR2GRAY)
        self.ret, self.s = cv2.threshold(self.s, 200, 255, cv2.THRESH_BINARY)
        cv2.imshow('frame', self.s)