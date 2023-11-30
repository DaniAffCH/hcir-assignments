import speech_recognition as sr
import sounddevice 
from transformers import pipeline

class SpeechRecognition():
    def __init__(self) -> None:
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone()
        self.recognizer.pause_threshold = 0.6
        self.sentimentClassifier = pipeline('sentiment-analysis')

    def listen(self):
        with self.mic as source:
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source, timeout=5)
            return self.recognizer.recognize_google(audio, language = 'en', show_all = True)
        
    def listenAndGetSentiment(self):
        sent = self.listen()
        if len(sent) > 0:
            sent = sent["alternative"][0]["transcript"]
            res = self.sentimentClassifier(sent)
            if res[0]['label'] == 'POSITIVE':
                return "yes", sent
            elif res[0]['label'] == 'NEGATIVE':
                return "no", sent
                
        return None, None
        
