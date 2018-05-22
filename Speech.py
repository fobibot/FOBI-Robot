import json

import os
from subprocess import PIPE, Popen

os_type = list(os.uname())[0]
if os_type == 'Linux': #RPi
    import aiy.cloudspeech
    from aiy.i18n import set_language_code
    import aiy.audio
    custom_dict_dir = "/home/pi/new/thesis/custom_dict.txt"
elif os_type == 'Darwin':
    import speech_recognition as sr
    custom_dict_dir = "/Users/arsapol/thesis/custom_dict.txt"

class Speech():
    def __init__(self, expect_phrase):
        self.expect_phrase = expect_phrase

        if os_type == 'Linux': #RPi
            set_language_code("th-TH")
            self.recognizer = aiy.cloudspeech.get_recognizer()
            aiy.audio.get_recorder().start()

            for phrase in self.expect_phrase:
                self.recognizer.expect_phrase(phrase)

        else:
            # self.GOOGLE_CLOUD_SPEECH_CREDENTIALS = self._read_credential_file(r"/home/pi/cloud_speech.json")
            self.GOOGLE_CLOUD_SPEECH_CREDENTIALS = self._read_credential_file(r"/Users/arsapol/cloud_speech.json")

            self.m = sr.Microphone()
            self.r = sr.Recognizer()

        # # Snowboy Configs
        # snowboy_dir = "/home/pi/snowboy/swig/Python3"
        # snowboy_model = ["/home/pi/snowboy/resources/models/FOBI.pmdl"]
        # self.snowboy_config = snowboy_dir, snowboy_model


    # def waiting_for_hotword(self):
    #     print("Waiting for hotword")
    #     with self.m as source:
    #         self.r.listen(source, snowboy_configuration=self.snowboy_config)
    #     print("**************** Got Hotword! ****************")
        
    #     return True

    if os_type == 'Linux': #RPi
        def listen_to_gcloud(self, immediate=False):
            print("Listening...")
            try:
                sentence = self.recognizer.recognize(immediate=immediate)
                if sentence != None and sentence != '':
                    print("Google Cloud Speech thinks you said : " + sentence)
                return sentence if (sentence != '' and sentence != None) else " "
            finally:
                print("Some error happended with speech recognition")
                return " "

    else: # osx
        def listen_to_gcloud(self, timeout=8):
            with self.m as source:
                print("Say something!")
                audio = self.r.listen(source, timeout=timeout)

            try:
                sentence = self.r.recognize_google_cloud(audio, credentials_json=self.GOOGLE_CLOUD_SPEECH_CREDENTIALS, language='th-TH', preferred_phrases=self.expect_phrase)
                # sentence = self.r.recognize_google_cloud(audio, credentials_json=self.GOOGLE_CLOUD_SPEECH_CREDENTIALS, language='th-TH')
                print("Google Cloud Speech thinks you said " + sentence)
                return sentence
            except sr.UnknownValueError:
                print("Google Cloud Speech could not understand audio")
                return " "
            except sr.RequestError as e:
                print("Could not request results from Google Cloud Speech service; {0}".format(e))

        def _read_credential_file(self, credential_dir):
            with open(credential_dir, "r") as f:
                credential = f.read()
            return credential

        def CalibrateMicNoiseThreshold(self):
            with self.m as source:
                self.r.adjust_for_ambient_noise(source)
            print("Set minimum energy threshold to {}".format(self.r.energy_threshold))

    

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
