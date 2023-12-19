import speech_recognition as sr
import sounddevice 
import whisper
import sounddevice as sd
import numpy as np
import tempfile
import soundfile as sf
from transformers import pipeline

class SpeechRecognition():
    def __init__(self) -> None:
        self.sample_rate = 44100
        self.channels = 2
        self.sttModel = whisper.load_model("small.en")
        self.sentimentClassifier = pipeline('sentiment-analysis')

    def listen(self, duration=5, isDebug=False):
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=not isDebug) as temp_file:
            temp_filename = temp_file.name

            recording = sd.rec(int(duration * self.sample_rate), samplerate=self.sample_rate, channels=self.channels, dtype='int16')
            print("Speak Now!")
            sd.wait()
            print("Stop Speaking!")

            sf.write(temp_filename, recording, self.sample_rate)
            
            result = self.sttModel.transcribe(temp_filename)
        
        return result["text"]

    def listenAndGetSentiment(self, duration=5):
        sent = self.listen(duration)
        if sent and len(sent) > 0:
            res = self.sentimentClassifier(sent)
            if res[0]['label'] == 'POSITIVE':
                return "yes", sent
            elif res[0]['label'] == 'NEGATIVE':
                return "no", sent
                
        return None, None
        