import smbus
import Adafruit_PCA9685
import struct
from imutils.video.pivideostream import PiVideoStream
from picamera.array import PiRGBArray
from picamera import PiCamera
import imutils
import time
import cv2
def num2byte(num):
    return [b for i in num for b in struct.pack('<h',i)]
def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

class i2c:
    def __init__(self,addr):
        self.bus = smbus.SMBus(1)
        self.addr = addr
    def write(self,cmd,data):
        try:
            self.bus.write_block_data(self.addr,cmd,data)
        except IOError:
            pass
    def write_low_high(self,cmd,data):
        try:
            self.bus.write_block_data(self.addr,cmd,num2byte(data))
        except IOError:
            pass

class fobi:
    def __init__(self):
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(60)
        self.face_cascade = cv2.CascadeClassifier('lbpcascade_frontalface.xml')
        self.vs = PiVideoStream().start()
        self.pos = 0
        time.sleep(2.0)
    def stop(self):
        self.vs.stop()
        cv2.destroyAllWindows()
    def motion(self,motion):
        if motion == 'joy':
            self.i2c.write(0x01,[0])
        elif motion == 'sad':
            self.i2c.write(0x01,[1])
        elif motion == 'angry':
            self.i2c.write(0x01,[2])
        elif motion == 'fear':
            self.i2c.write(0x01,[3])
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
            data = int(map(face_center['x'],0,320,-300,300))
            if not(data>-50 and data <50):
                self.pos = (self.pos+data)
            if self.pos < -300:
                self.pos = -300
            elif self.pos > 300:
                self.pos = 300
            move = self.pos+500
            print(move,data)
            self.pwm.set_pwm(0, 0,move)
            #self.i2c.write_low_high(0x02,[face_center['x'],face_center['y']])
        return size
