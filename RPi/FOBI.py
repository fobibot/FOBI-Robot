import os

import aiy.audio
import aiy.cloudspeech

from subprocess import PIPE, Popen

class Robot:
    def __init__(self):
        self.thai = "th"
        self.english = "en-US"
        
        self.recognizer = aiy.cloudspeech.get_recognizer()
        aiy.audio.get_recorder().start()

    def Listen(self):
        return self.recognizer.recognize()  # return text

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
        if process:
            cmd += ['speed', '3']
        else:
            cmd += ['speed', '1.3']
        print(cmd)
        self.speaker = self._create_task(cmd=cmd)
        if wait:
            self.speaker.wait()

    def _create_task(self, cmd):
        return Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True, preexec_fn=os.setsid)

    def Speak_Advance(self, sentence, _lang="en-US", _volume=10, _pitch=None):
        # Support Language : en-US, en-GB, de-DE, es-ES, fr-FR, it-IT
        return aiy.audio.say(sentence, lang=_lang, volume=_volume, pitch=_pitch)
