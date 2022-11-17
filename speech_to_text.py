import os 
import requests 
import json 
import logging as Logger
from google.cloud import speech

"""
  file to access Google-Speech-to-Text API 
"""


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'single-inquiry-368223-c15d6b2b387e.json'
speech_client = speech.SpeechClient()

# Transcribe local media file 
# using recognition audio resource 
media_file_name_wav = 'demo audio.wav' #note this will be what henry figures out in arduino

