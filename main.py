import FOBI
import time as t
from New_ML.Predict import Prediction
from pythainlp.tokenize import word_tokenize

# start running function for the first time
robot = FOBI.Robot()
predict = Prediction()
sentence = robot.Listen()
sentence = "เริ่มทำงาน"
predict.Predict(sentence)

start_listen = False

while 1:
    # if start_listen:
    input("Enter to start")
    sentence = robot.Listen()
    print(sentence)

    predicted_sentence = predict.Predict(sentence)


    _object = ""
    _place = ""
    if predicted_sentence == "ข้อมูล-คน" or predicted_sentence == "สถานที่-คน" or predicted_sentence == "บุคคล":
        try:
            sentence = word_tokenize(sentence, engine='deepcut')
            sentence = [x for x in sentence if x != ' '] # remove all blank spaces
            print("Word cut sentence :", sentence)
            for i, word in enumerate(sentence):
                if word in robot.title_names:
                    _object = sentence[i+1]
                    print("_object :", _object)
                    break
            if _object == None:
                print("Cannot Detect Person")
                _object = "No"

            _place = "FBสามศูนย์ห้า" # edit to find in database next time
            
            
            predicted_sentence += " " + _object + " " + _place
            print("To RiveScript :",predicted_sentence)
            answer = robot.Reply(predicted_sentence)
            robot.Speak(answer, robot.thai)
            start_listen = False
        except TypeError:
            pass
    elif predicted_sentence == "สถานที่-สถานที่":
        try:
            sentence = word_tokenize(sentence, engine='deepcut')
            sentence = [x for x in sentence if x != ' '] # remove all blank spaces
            print("Word cut sentence :", sentence)
            for i, word in enumerate(sentence):
                if word in "ห้อง":
                    _object = sentence[i+1]
                    print("_object :", _object)
                    break
            if _object == None:
                print("Cannot Detect Person")
                _object = "No"

            _place = "สาม" # edit to find in database next time
            
            
            predicted_sentence += " " + _object + " " + _place
            print("To RiveScript :",predicted_sentence)
            answer = robot.Reply(predicted_sentence)
            robot.Speak(answer, robot.thai)
            start_listen = False
        except TypeError:
            pass