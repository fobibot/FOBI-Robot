import os

import codecs
import json

from deepcut import tokenize

import Speech

os_type = list(os.uname())[0]
if os_type == 'Linux': #RPi
    from action import action
    custom_dict_dir = "/home/pi/new/thesis/custom_dict.txt"
else:
    custom_dict_dir = "/Users/arsapol/thesis/custom_dict.txt"

from rivescript import RiveScript

class Robot:
    def __init__(self):
        print("Initialize Robot")
        self.thai = "th"
        self.english = "en"
        self.robot_name = "FO BEE"

        # Load Datas.json files

        self.PeopleInformation = self.LoadJsonFile('New_ML/Special_Names/PeopleInformation.json')
        self.NameToKeyword = self.LoadJsonFile('New_ML/Special_Names/NameToKeyword.json')
        self.RoomInformation = self.LoadJsonFile('New_ML/Special_Names/RoomInformation.json')
        self.RoomNameToKeyword = self.LoadJsonFile('New_ML/Special_Names/RoomNameToKeyword.json')
        
        self.title_names = self.LoadDatabaseFile(filename='New_ML/Special_Names/Title_Names.csv')
        # self.title_names = self.LoadJsonFile('New_ML/Special_Names/Title_Names.json')
        
        # Setup Speech - Google Cloud Speech and Text to Speech
        self.Speech = Speech.Speech(list(self.NameToKeyword.keys()))
        

        # Load RiveScript
        self._chatter = RiveScript(utf8=True)
        self._chatter.load_directory("RiveScript")
        self._chatter.sort_replies()

    # def word_tokenize(self, text):
    #     return tokenize(text, custom_dict=self.custom_dict_dir)
        
    def LoadRobotMotion(self):
        if os_type == 'Linux': #RPi
            self.Motion = action.action(camera=False)
        self.Motion.motion("curious") # -> sad, happy, angry, normal, curious
        
    def LoadJsonFile(self, filename):
        try:
            with open(filename) as json_data:
                json_file = json.load(json_data)
        except:
            print("No file name", filename, ".json")
            pass
        return json_file

    def LoadDatabaseFile(self, filename):
        with codecs.open(filename, 'r',encoding='utf-8-sig') as f:
            lines = f.read().splitlines()

        return lines

    def SpeakAndReply(self, text):
        answer = self._chatter.reply("localuser", text)
        
        try:
            answer = answer.split(',')
            emotion = answer[1]
            answer = answer[0]
            if os_type == 'Linux': #RPi
                self.Motion.motion(emotion)
            print("Robot Feeling is", emotion)
        except IndexError:
            print("Something wrong with emotion in \'text.rive\' or \'action.py\'")
            print("Error in SpeakAndReply function : answer = ", answer[0])
            answer = answer[0]
            emotion = "curious"
            if os_type == 'Linux': #RPi
                self.Motion.motion(emotion)
            
        if answer == "FO BEE":
            self.Speech.Speak(answer, self.english, wait=True, robot_name=True)
        else:
            self.Speech.Speak(answer, self.thai, wait=True)

def word_tokenize(text):
    return tokenize(text, custom_dict=custom_dict_dir)