import time as t
import os
os_type = list(os.uname())[0]
from New_ML.Predict import Prediction
start = t.time()
import FOBI
print("Loaded FOBI.py time :", t.time()-start)

# start running function for the first time
start = t.time()
robot = FOBI.Robot()
print("Initial FOBI time :", t.time()-start)

start = t.time()
predict = Prediction(confidence_value = 0.77)
print("Initial Prediction time :", t.time()-start)


sentence = "เริ่มทำงาน"
start = t.time()
predict.Predict(sentence)
print("First Prediction time :", t.time()-start)

# robot.Speech.CalibrateMicNoiseThreshold()

start_listen = False

def SecondTry(sentence):
    global start_listen

    wordcut_sentence = robot.word_tokenize(sentence)
    second_try_sentence = " ".join(wordcut_sentence)
    robot.SpeakAndReply(second_try_sentence)
    start_listen = False

def FindPlaceNameInSentence(predicted_sentence, sentence):
    _object = None
    _place = None
    _keyword = None
    try:
        sentence = robot.word_tokenize(sentence)
        sentence = [x for x in sentence if x != ' '] # remove all blank spaces
        print("Word cut sentence :", sentence)
        for i, word in enumerate(sentence):
            if word in "ห้อง":
                try:
                    _keyword = sentence[i+1]
                    print("_keyword :", _keyword)
                    _object = robot.RoomNameToKeyword[_keyword]
                    _place = robot.RoomInformation[_object]
                except (NameError, KeyError):
                    print("*"*5, "Found Some error in file \'RoomNameToKeyword.json\' or \'RoomInformation.json\'", "*"*5)
                    pass
                break
    except TypeError:
        pass

    if _object != None: # Cannot Detect Place
        predicted_sentence += " " + _object + " " + _place
    else:
        try:
            predicted_sentence = "ไม่รู้จักสถานที่ " + _keyword
        except TypeError:
            predicted_sentence = sentence # waiting for second try
            pass

    return predicted_sentence

def FindPersonNameInSentence(predicted_sentence, sentence):
    _object = None
    _place = None
    _keyword = None
    try:
        sentence = robot.word_tokenize(sentence)
        sentence = [x for x in sentence if x != ' '] # remove all blank spaces
        print("Word cut sentence :", sentence)
        for i, word in enumerate(sentence):
            if word in robot.title_names: # found title names # if word in robot.title_names["Title_Name"]:
                print("-------------- Case 1 --------------")
                try:
                    _keyword = sentence[i+1]
                    _type, _object = robot.NameToKeyword[_keyword]
                    _place = robot.PeopleInformation[_type][_object]["room"][0] # choose first room in the list -> shown that person always there
                except (NameError, KeyError):
                    print("*"*5, "Found some error in file \'PeopleInformation.json\' or Cannot Detect Person", "*"*5)
                    pass
                break # i'm not sure, will this work?

        if _object != None:
            print("-------------- Case 2 --------------")
            predicted_sentence += " " + _object + " " + _place
        else:
            for i, word in enumerate(sentence):
                if word in list(robot.NameToKeyword.keys()): # try to find fibo names in collected data
                    print("-------------- Case 3 --------------")
                    try:
                        _keyword = word
                        _type, _object = robot.NameToKeyword[_keyword]
                        _place = robot.PeopleInformation[_type][_object]["room"][0] # choose first room in the list -> shown that person always there
                        predicted_sentence += " " + _object + " " + _place
                    except (NameError, KeyError):
                        print("*"*5, "Found some error in file \'PeopleInformation.json\' or Cannot Detect Person", "*"*5)
                        pass
                    break # i'm not sure, will this work?
            if _object == None:
                print("-------------- Case 4 --------------")
                try:
                    predicted_sentence = "ไม่รู้จักคน " + _keyword
                except TypeError:
                    # predicted_sentence = "ไม่เข้าใจที่พูด"
                    predicted_sentence = sentence
                    pass

    except TypeError:
        pass

    return predicted_sentence

while 1:
    sentence = None
    count_cannot_recognize_time = 0
    # if __debug__:
    #     sentence = input("Type some sentence : ") 
    # else:
    while 1:
        if not start_listen:
            if os_type == 'Linux': #RPi
                if robot.Motion.face_detected():
                    start_listen = True
            else:
                input("Enter to listen...")
                start_listen = True
        else:
            if count_cannot_recognize_time == 0:
                robot.SpeakAndReply("ทักทาย")
            print("listening...")
            sentence = robot.Speech.listen_to_gcloud()
            if sentence != '' and sentence != ' ':
                print("------ Case 1 -------")
                start_listen = True
                break
            else:
                print("------ Case 2 -------")
                if count_cannot_recognize_time >= 3:
                    robot.SpeakAndReply("ไม่ได้พูด") # user didn't say anything
                    start_listen = False
                    # break
                robot.SpeakAndReply("ไม่เข้าใจที่พูด")
                count_cannot_recognize_time += 1

    
    predicted_sentence = predict.Predict(sentence)

    try:
        _object = None
        _place = None
        if predicted_sentence == "ข้อมูล-คน" or predicted_sentence == "สถานที่-คน" or predicted_sentence == "บุคคล":
            predicted_sentence = FindPersonNameInSentence(predicted_sentence, sentence)
            
            print("To RiveScript :", predicted_sentence)
            robot.SpeakAndReply(predicted_sentence)
            start_listen = False

        elif predicted_sentence == "สถานที่-สถานที่":
            predicted_sentence = FindPlaceNameInSentence(predicted_sentence, sentence)
            
            print("To RiveScript :", predicted_sentence)
            robot.SpeakAndReply(predicted_sentence)
            start_listen = False

        else:
            SecondTry(sentence)

    except TypeError:
        SecondTry(sentence)
