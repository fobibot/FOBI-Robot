import os

import codecs
import json

import Speech
os_type = list(os.uname())[0]
if os_type == 'Linux': #RPi
    from action import action

from rivescript import RiveScript

# from subprocess import PIPE, Popen

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
        
        if os_type == 'Linux': #RPi
            self.Motion = action.action()
        # self.Motion.motion("sad") -> sad, happy, angry, normal, curious

        # Load RiveScript
        self._chatter = RiveScript(utf8=True)
        self._chatter.load_directory("RiveScript")
        self._chatter.sort_replies()
        
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
            print("Error in SpeakAndReply function : answer = ", answer)
            
        if answer == "FO BEE":
            self.Speech.Speak(answer, self.english, wait=True, robot_name=True)
        else:
            self.Speech.Speak(answer, self.thai, wait=True)