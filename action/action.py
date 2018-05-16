from subprocess import call
import Adafruit_PCA9685
from action.SSD1331 import SSD1331
import struct
import sys
import imutils
import time
import cv2
import random
import os
import picamera.exc
from threading import Thread
os = os.uname()[4][:3]
if os == 'arm':
    from imutils.video.pivideostream import PiVideoStream
else:
    from imutils.video import WebcamVideoStream

SSD1331_PIN_CS  = 23
SSD1331_PIN_DC  = 24
SSD1331_PIN_RST = 25

class action:
    def __init__(self,debug=False,camera=True,servo=True):
        self.debug = debug
        self._camera = camera
        self._servo = servo

        if os == 'arm':
            try:
                if self._camera:
                    self.vs = PiVideoStream().start()
            except picamera.exc.PiCameraError:
                self._camera = False
                print('Picamera Not Found')
            try:
                if self._servo:
                    self.pwm = Adafruit_PCA9685.PCA9685()
                    self.pwm.set_pwm_freq(60)
            except OSError:
                self._servo = False
                print('PCA9685 Not Found')
            self.eye = SSD1331(SSD1331_PIN_DC, SSD1331_PIN_RST, SSD1331_PIN_CS)
            self.eye_start()
        else:
            if self._camera:
                self.vs = WebcamVideoStream(src=0).start()
        self.face_cascade = cv2.CascadeClassifier('/home/pi/FOBI/action/data/lbpcascade_frontalface_improved.xml')
        self.pos = 500
        self.pos_y =450
        self.time = 0
        self.stopped = False
        self.end = False
        self._face_detected = False
        self.servo = {
        'roll':{'pin':3,'min':370,'cen':305,'max':200}, #เอียงคอ    ซ้าย ขวา กลาง
        'pich':{'pin':2,'min':350,'cen':450,'max':550}, #ก้มหน้า    เงย กลาง    ก้ม
        'yaw':{'pin':4,'min':200,'cen':300,'max':450},  #คอ     ขวา กลาง ซ้าย
        'left_eyebrow':{'pin':1,'min':450,'cen':550,'max':610},     #คิ้วซ้าย
        'right_eyebrow':{'pin':0,'min':550,'cen':460,'max':400},    #คิ้วขวา
        'left_tentacle':{'pin':6,'min':400,'max':250},  #หนวดซ้าย   หย่อน   ตึง
        'right_tentacle':{'pin':7,'min':470,'max':650}, #หนวดขวา    หย่อน   ตึง
        }
        # self.motion('normal')

        time.sleep(2.0)
        if self._camera:
            self.frame = self.vs.read()
            self.tracking_start()

    def tracking_start(self):
        t = Thread(target=self.tracking_update, args=())
        t.daemon = True
        t.start()
        return self
    def face_detected(self):
        return self._face_detected
    def eye_start(self):
        self.eye_time = time.time()
        self.old_eye_state = ''
        self.eye_state = 'normal'
        self.eye_num = 1
        t = Thread(target=self.eye_update, args=())
        t.daemon = True
        t.start()
        return self
    def servo2motion(self,name,pos,offset=0,side=''):
        if os == 'arm' and self._servo:
            self.log('servo',name,pos,offset,side)
            if side != '':
                if type(pos) != str:
                    self.pwm.set_pwm(self.servo[name]['pin'], 0, pos)
                else:
                    self.pwm.set_pwm(self.servo[name]['pin'], 0, self.servo[name][pos]+offset)
            else:
                if name == 'yaw' or name == 'pich' or name == 'roll':
                    if type(pos) != str:
                        self.pwm.set_pwm(self.servo[name]['pin'], 0, pos+offset)
                    else:
                        self.pwm.set_pwm(self.servo[name]['pin'], 0, self.servo[name][pos]+offset)
                else:
                    if type(pos) != str:
                        self.pwm.set_pwm(self.servo['left_'+name]['pin'], 0, pos+offset)
                        self.pwm.set_pwm(self.servo['right_'+name]['pin'], 0, pos+offset)
                    else:
                        self.pwm.set_pwm(self.servo['left_'+name]['pin'], 0, self.servo['left_'+name][pos]+offset)
                        self.pwm.set_pwm(self.servo['right_'+name]['pin'], 0, self.servo['right_'+name][pos]+offset)
        else:
            self.log('servo',name,pos,offset,side)
    def log(self,*var):
        if self.debug:
            print(var)
    def imshow(self):
        if os != 'arm':
            cv2.imshow('frame',self.frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.end = True
        else:
            return self
    def waitKey(self):
        return self.end
    def stop(self):
        self.eye.EnableDisplay(False)
        self.eye.Remove()
        if self._camera:
            self.stopped = True
            #cv2.destroyAllWindows()
            self.vs.stop()


    def motion(self,motion):
        if motion == 'joy':
            self.servo2motion('tentacle','max')
            self.servo2motion('eyebrow','max')
        elif motion == 'sad':
            self.servo2motion('tentacle','min')
            self.servo2motion('eyebrow','min')
        elif motion == 'angry':
            self.servo2motion('tentacle','max')
            self.servo2motion('eyebrow','min')
        elif motion == 'fear':
            self.servo2motion('tentacle','min')
            self.servo2motion('eyebrow','cen')
            self.servo2motion('yaw','cen',-100)
        elif motion == 'normal':
            self.servo2motion('tentacle','min')
            self.servo2motion('eyebrow','cen')
            self.servo2motion('yaw','cen')
            self.servo2motion('roll','cen')
            self.servo2motion('pich','cen',10)
        self.eye_motion(motion)
    def eye_motion(self,name,num=1):
        self.eye_state = name
        self.eye_num = num
    def eye_update(self):
        while True:
            if self.eye_state == 'sad':
                self.eye.Blink(self.eye_state)
            else:
                if self.eye_state != self.old_eye_state:
                    self.eye.Emotion(self.eye_state)
                if time.time() - self.eye_time > 0.1 and time.time() - self.eye_time < 0.2:
                    self.eye.Blink(self.eye_state)
                    self.eye.Blink(self.eye_state)
                if time.time() - self.eye_time > 5 and time.time() - self.eye_time < 5.1:
                    self.eye.Blink(self.eye_state)
                if time.time() - self.eye_time > 6:
                    self.eye_time = time.time()
            time.sleep(0.05)
    def tracking_update(self):
        while True:
            self.frame= self.vs.read()
            self.frame= imutils.resize(self.frame,width=320)

            gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 2)
            face_center = {}
            size = 0
            for (x,y,w,h) in faces:
                if w*h>size and w*h >1000:
                    face_center['x'] = int(x+w/2)
                    face_center['y'] = int(y+h/2)
                    size = w*h
                    cv2.rectangle(self.frame,(x,y),(x+w,y+h),(255,0,0),2)
                    cv2.circle(self.frame,(face_center['x'],face_center['y']),10,(255,0,0),-1)
            if(len(faces)>0 and size>1000):
                call(["aplay","/home/pi/b.wav"])
                frame_x = 320/2
                frame_y = 240/2
                margin = frame_x - face_center['x']
                margin_y = frame_y - face_center['y']
                gap = 40
                gap_y = 40
                self._face_detected = True
                #self.log(margin,margin_y,self.pos_y)
                if margin > gap:
                    self.pos += 15
                    if self.pos >= 800:
                        self.pos = 800
                    self.servo2motion('yaw',self.pos)
                elif margin < gap*-1:
                    self.pos -= 15
                    if self.pos <= 200:
                        self.pos = 200
                    self.servo2motion('yaw',self.pos)
                if margin_y > gap_y:
                    self.pos_y -= 13
                    if self.pos_y <= 300:
                        self.pos_y = 300
                    self.servo2motion('pich',self.pos_y)
                elif margin_y < gap_y*-1:
                    self.pos_y += 13
                    if self.pos_y >= 500:
                        self.pos_y = 500
                    self.servo2motion('pich',self.pos_y)
            else:
                self._face_detected = False
            #     self.log('Not Found')

            # self.imshow()
            if self.stopped:
                return


            # elif margin > gap*-1 and margin < gap:
            #     a =0
            #self.log(self.pos)
            #self.i2c.write_low_high(0x02,[face_center['x'],face_center['y']])


if __name__ == "__main__":
    action = action(debug=True,camera=True,servo=True)

    #a = input()
    while True:
        # input('HI')
        # if fobi.waitKey():
        #     break
        #motion = input('Input:')
        #if motion == 'q':
      #      break
        action.motion('normal')
        time.sleep(10)
        action.motion('angry')
        time.sleep(10)
        action.motion('happy')
        time.sleep(10)
        action.motion('sad')
        time.sleep(10)


    action.stop()
