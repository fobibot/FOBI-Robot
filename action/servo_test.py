import Adafruit_PCA9685
pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(60)
servo = {
'roll':{'pin':0,'min':0,'max':100},
'pich':{'pin':0,'min':0,'max':100},
'yaw':{'pin':0,'min':0,'max':100},
'left_eyebrow':{'pin':0,'min':0,'max':100},
'right_eyebrow':{'pin':0,'min':0,'max':100},
'left_tentacle':{'pin':0,'min':0,'max':100},
'right_tentacle':{'pin':1,'min':0,'max':100},
}
while True:
    num = input('num:')
    pos = input('pos:')
    pwm.set_pwm(int(num), 0, int(pos))
