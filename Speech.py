import json

import os
from subprocess import PIPE, Popen

import speech_recognition as sr

class Speech():
    def __init__(self, expect_phrase):
        self.GOOGLE_CLOUD_SPEECH_CREDENTIALS = self._read_credential_file(r"~/cloud_speech.json")
        self.expect_phrase = expect_phrase

        # Snowboy Configs
        snowboy_dir = "~/snowboy/swig/Python3"
        snowboy_model = ["~snowboy/resources/models/snowboy.umdl"]
        self.snowboy_config = snowboy_dir, snowboy_model

        self.m = sr.Microphone()
        self.r = sr.Recognizer()

    def _read_credential_file(self, credential_dir):
        with open(credential_dir, "r") as f:
            credential = f.read()
        return credential

    def CalibrateMicNoiseThreshold(self):
        with self.m as source:
            self.r.adjust_for_ambient_noise(source)
        print("Set minimum energy threshold to {}".format(self.r.energy_threshold))

    def waiting_for_hotword(self):
        print("Waiting for hotword")
        with sr.Microphone() as source:
            self.r.listen(source, snowboy_configuration=self.snowboy_config)
        print("**************** Got Hotword! ****************")
        
        return True

    def listen_to_gcloud(self, timeout=8):
        with sr.Microphone() as source:
            audio = self.r.listen(source, timeout=timeout)
        
        try:
            sentence = self.r.recognize_google_cloud(audio, credentials_json=self.GOOGLE_CLOUD_SPEECH_CREDENTIALS, language='th-TH', preferred_phrases=self.expect_phrase)
            # sentence = self.r.recognize_google_cloud(audio, credentials_json=self.GOOGLE_CLOUD_SPEECH_CREDENTIALS, language='th-TH')
            print("Google Cloud Speech thinks you said " + sentence)
            return sentence
        except sr.UnknownValueError:
            print("Google Cloud Speech could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Cloud Speech service; {0}".format(e))


    # Speak Zone
    def Speak(self, sentence, lang, wait=False, process=False, speak_volume=10, robot_name=False):
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
            cmd += ['speed', '2.0']
        else:
            if not robot_name:
                cmd += ['speed', '1.3']
            else:
                cmd += ['speed', '1.0']
        print(cmd)
        self.speaker = self._create_task(cmd=cmd)
        if wait:
            self.speaker.wait()

    def _create_task(self, cmd):
        return Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True, preexec_fn=os.setsid)