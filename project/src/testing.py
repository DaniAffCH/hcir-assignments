# JUST FOR DEVELOPMENT TESTS, DELETE IN PRODUCTION

from speech.recognition import SpeechRecognition
from filter.filter import BadWordsFilter

TESTING_BW = False
TESTING_SENT = True

print("Loading...")

s = SpeechRecognition()
bwFilter = BadWordsFilter("filter/GoogleNews-vectors-negative300.bin")

print("Loaded!")
while True:
    if TESTING_BW:
        out = s.listen()
        if len(out) > 0:
            sentence = out["alternative"][0]["transcript"]
            print(sentence)
            res, bw = bwFilter.processSentence(sentence)
            print(f"Does it contain any badword? {res} -> {bw}")
    
    if TESTING_SENT:
        meaning, sentence = s.listenAndGetSentiment()
        if meaning is not None:
            print(sentence)
            print(f"It means -> {meaning}")

