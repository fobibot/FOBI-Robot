import FOBI
import time as t
from New_ML.Predict import Prediction
from pythainlp.tokenize import word_tokenize

# start running function for the first time
robot = FOBI.Robot()
predict = Prediction()
if not __debug__:
    sentence = robot.Listen()
sentence = "เริ่มทำงาน"
predict.Predict(sentence)

start_listen = False

def FindPlaceNameInSentence():
    _object = None
    _place = None
    try:
        sentence = word_tokenize(sentence, engine='deepcut')
        sentence = [x for x in sentence if x != ' '] # remove all blank spaces
        print("Word cut sentence :", sentence)
        for i, word in enumerate(sentence):
            if word in "ห้อง":
                try:
                    _keyword = sentence[i+1]
                    print("_keyword :", _keyword)
                    _object = robot.RoomNameToKeyword[_keyword]
                    _place = robot.RoomInformation[_object]
                except NameError or KeyError:
                    print("*"*5, "Found Some error in file \'RoomNameToKeyword.json\' or \'RoomInformation.json\'", "*"*5)
                    pass
                break
    except TypeError:
        pass

    return _object, _place

while 1:
    # if start_listen:
    if __debug__:
        sentence = input("Type some sentence : ") 
    else:
        print("listening...")
        sentence = robot.Listen()
        print(sentence)

    predicted_sentence = predict.Predict(sentence)

    _object = None
    _place = None
    if predicted_sentence == "ข้อมูล-คน" or predicted_sentence == "สถานที่-คน" or predicted_sentence == "บุคคล":
        if predicted_sentence == "สถานที่-คน":

        try:
            sentence = word_tokenize(sentence, engine='deepcut')
            sentence = [x for x in sentence if x != ' '] # remove all blank spaces
            print("Word cut sentence :", sentence)
            for i, word in enumerate(sentence):
                if word in robot.title_names: # found title names # if word in robot.title_names["Title_Name"]:
                    print("-------------- Case 1 --------------")
                    try:
                        _keyword = sentence[i+1]
                        _type, _object = robot.NameToKeyword[_keyword]
                        _place = robot.PeopleInformation[_type][_object]["room"][0] # choose first room in the list -> shown that person always there
                    except NameError or KeyError:
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
                            _type, _object = robot.NameToKeyword[word]
                            _place = robot.PeopleInformation[_type][_object]["room"][0] # choose first room in the list -> shown that person always there
                            predicted_sentence += " " + _object + " " + _place
                        except NameError or KeyError:
                            print("*"*5, "Found some error in file \'PeopleInformation.json\' or Cannot Detect Person", "*"*5)
                            pass
                        break # i'm not sure, will this work?
                if _object == None:
                    print("-------------- Case 4 --------------")
                    predicted_sentence = "ไม่รู้จักคน " + _keyword
            
            print("To RiveScript :", predicted_sentence)
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
                    try:
                        _keyword = sentence[i+1]
                        print("_keyword :", _keyword)
                        _object = robot.RoomNameToKeyword[_keyword]
                        _place = robot.RoomInformation[_object]
                    except NameError or KeyError:
                        print("*"*5, "Found Some error in file \'RoomNameToKeyword.json\' or \'RoomInformation.json\'", "*"*5)
                        pass
                    break

            if _object != None: # Cannot Detect Person
                predicted_sentence += " " + _object + " " + _place
            else:
                predicted_sentence = "ไม่รู้จักสถานที่ " + _keyword
            print("To RiveScript :",predicted_sentence)
            answer = robot.Reply(predicted_sentence)
            robot.Speak(answer, robot.thai)
            start_listen = False
            
        except TypeError:
            pass