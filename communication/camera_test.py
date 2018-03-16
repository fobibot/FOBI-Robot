import numpy as np
import cv2
import imutils
import time
face_cascade = cv2.CascadeClassifier('lbpcascade_frontalface.xml')
cap = cv2.VideoCapture(0)
def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
pos = 400
while(True):
    ret, frame = cap.read()
    frame = imutils.resize(frame,width=400)
    #print(frame.shape)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 2)
    face_center = {}
    size = 0
    for (x,y,w,h) in faces:
        if w*h>size and w*h >1000:
            #print(w*h)
            face_center['x'] = int(x+w/2)
            face_center['y'] = int(y+h/2)
            size = w*h
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
            cv2.circle(frame,(face_center['x'],face_center['y']),10,(255,0,0),-1)
    if(len(faces)>0 and size>1000):
        data = int(map(face_center['x'],0,320,-300,300))
        if not(data>-50 and data <50):
            pos = (pos+data)
        if pos < -300:
            pos = -300
        elif pos > 300:
            pos = 300
        move = pos+500
        time.sleep(0.1)
        print(move,data)
    #print(face_center)
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
