# The following program uses google speech text
import speech_recognition as sr
sr.__version__
from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *
import pyaudio
import pocketsphinx

#r = sr.recognize_sphinx()
#mic = sr.Microphone()
sr.Microphone.list_microphone_names()
mic = sr.Microphone(device_index=3)
with mic as source:
    audio = r.listen(source)
