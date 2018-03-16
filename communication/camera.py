from __future__ import print_function
from imutils.video.pivideostream import PiVideoStream
from imutils.video import FPS
from picamera.array import PiRGBArray
from picamera import PiCamera
import argparse
import imutils
import time
import cv2
print("[INFO] sampling THREADED frames from `picamera` module...")
face_cascade = cv2.CascadeClassifier('lbpcascade_frontalface.xml')
vs = PiVideoStream().start()
time.sleep(2.0)


# loop over some frames...this time using the threaded stream
while True:
    frame = vs.read()
    frame = imutils.resize(frame,width=400)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 2)
    face_center = {}
    size = 0
    for (x,y,w,h) in faces:
        if w*h>size and w*h >1000:
            face_center['x'] = int(x+w/2)
            face_center['y'] = int(y+h/2)
            size = w*h
    print(face_center)
cv2.destroyAllWindows()
vs.stop()
def tracking(self):
    frame = self.vs.read()
    frame = imutils.resize(frame,width=320)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = self.face_cascade.detectMultiScale(gray, 1.1, 2)
    face_center = {}
    size = 0
    for (x,y,w,h) in faces:
        if w*h>size and w*h >1000:
            face_center['x'] = int(x+w/2)
            face_center['y'] = int(y+h/2)
            size = w*h
    if(len(faces)>0 and size>1000):
        # print(face_center)
        frame_x = 320/2
        frame_y = 240/2
        margin = frame_x - face_center['x']
        gap = 30

        if margin > gap:
            #print('Right')
            self.pos += 8
            if self.pos >= 800:
                self.pos = 800
            self.pwm.set_pwm(0, 0, self.pos)
        elif margin < gap*-1:
            #print('Left')
            self.pos -= 8
            if self.pos <= 200:
                self.pos = 200
            self.pwm.set_pwm(0, 0, self.pos)
        elif margin > gap*-1 and margin < gap:
            a =0
        print(self.pos)

        #self.i2c.write_low_high(0x02,[face_center['x'],face_center['y']])
    return size
