import FOBI
import time as t

robot = FOBI.Robot()

robot.Speak("สวัสดี เราชื่อ ลูกพีช คนสวย", lang=robot.thai)
# robot.Speak_Advance("Hello")

t.sleep(5)
