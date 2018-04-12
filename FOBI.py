import os

import codecs
import json

import aiy.audio
import aiy.cloudspeech
from aiy.i18n import set_language_code

from rivescript import RiveScript

from subprocess import PIPE, Popen

class Robot:
    def __init__(self):
        print("Initialize Robot")
        self.thai = "th"
        self.english = "en"
        self.robot_name = "FO BEE"
        set_language_code("th-TH")
        
        self.recognizer = aiy.cloudspeech.get_recognizer()
        self.LoadExpectWords()
        aiy.audio.get_recorder().start()

        self._chatter = RiveScript(utf8=True)
        self._chatter.load_directory("RiveScript")
        self._chatter.sort_replies()

        # self.title_names = self.LoadTitleNames()
        # self.room_names = self.LoadRoomNames()

        try:
            with open('New_ML/Special_Names/PeopleInformation.json') as json_data:
                self.PeopleInformation = json.load(json_data)
        except:
            print("No file name \'PeopleInformation.json\'")

        try:
            with open('New_ML/Special_Names/NameToKeyword.json') as json_data:
                self.NameToKeyword = json.load(json_data)
        except:
            print("No file name \'NameToKeyword.json\'")
        
        self.title_names = self.LoadDatabaseFile(filename='New_ML/Special_Names/Title_Names.csv', add_expect_word=True, need_return=True)
        # self.room_names = self.LoadDatabaseFile(filename='New_ML/Special_Names/Room_Names.csv', add_expect_word=True, need_return=True)

    def LoadDatabaseFile(self, filename, add_expect_word, need_return):
        with codecs.open(filename, 'r',encoding='utf-8-sig') as f:
            lines = f.read().splitlines()
        
        if(add_expect_word):
            for word in lines:
                self.recognizer.expect_phrase(word)
        
        return lines

    def LoadExpectWords(self):
        print("Adding Expected Words to Google Speech")
        with codecs.open('New_ML/Special_Names/FIBO_member_G_names.csv', 'r',encoding='utf-8-sig') as f:
            lines = f.read().splitlines()
        # print(lines)
        for name in lines:
            self.recognizer.expect_phrase(name)

    def Listen(self):
        print("Listening...")
        sentence = self.recognizer.recognize()
        print("End of Listening")
        return sentence #if type(sentence) == type.__str__ else "" # return text

    def Speak(self, sentence, lang, wait=False, process=False, speak_volume=10):
        print("Speak:", sentence)
        cmd = ['google_speech', '-l', lang, sentence]
        cmd += ['--sox-effects', 'gain', str(speak_volume)]
        if process:
            cmd += ['pitch', '50']
            cmd += ['stretch', '2.5', '133.33']
            cmd += ['lin', '0.2', '0.4']
            cmd += ['overdrive', '25', '25']
            cmd += ['echo', '0.4', '0.8', '15', '0.8']
            cmd += ['synth', 'sine', 'fmod', '30']
            cmd += ['speed', '1.3']
        print(cmd)
        self.speaker = self._create_task(cmd=cmd)
        if wait:
            self.speaker.wait()

    def _create_task(self, cmd):
        return Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True, preexec_fn=os.setsid)

    def Speak_Advance(self, sentence, _lang="en-US", _volume=75, _pitch=None):
        # Support Language : en-US, en-GB, de-DE, es-ES, fr-FR, it-IT
        return aiy.audio.say(sentence, lang=_lang, volume=_volume, pitch=_pitch)

    def Reply(self, text):
        return self._chatter.reply("localuser", text)
