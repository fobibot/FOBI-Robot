import FOBI
import time as t
# from New_ML.Predict import Prediction

import snowboy.snowboydecoder as snowboydecoder
import sys
import signal
import os

interrupted = False

robot = None
predict = None
detector = None

import aiy.audio

def detectedCallback():
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted


model = "snowboy/resources/models/snowboy.umdl"

detector = snowboydecoder.HotwordDetector(model, sensitivity=0.38)
print('Listening... Press Ctrl+C to exit')

# main loop
while 1:
    detector.start(detected_callback=detectedCallback,
                interrupt_check=interrupt_callback,
                sleep_time=0.01)
    detector.terminate()

    robot = FOBI.Robot()
    # predict = Prediction()
    sentence = robot.Listen()
    # sentence = "สวัสดีจ้า"
    # predict.Predict(sentence)

    aiy._drivers._recorder.Recorder().stop()
    detector.terminate()
    interrupted = False