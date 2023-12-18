# JUST FOR DEVELOPMENT TESTS, DELETE IN PRODUCTION

from speech.recognition import SpeechRecognition
from filter.filter import BadWordsFilter

TESTING_BW = True
TESTING_SENT = False

print("Loading...")

s = SpeechRecognition()
bwFilter = BadWordsFilter("filter/GoogleNews-vectors-negative300.bin")

print("Loaded!")
while True:
    if TESTING_BW:
        out = s.listen()
        if out and len(out) > 0:
            print(out)
            res, bw = bwFilter.processSentence(out)
            print(f"Does it contain any badword? {res} -> {bw}")
    
    if TESTING_SENT:
        meaning, sentence = s.listenAndGetSentiment()
        if meaning is not None:
            print(sentence)
            print(f"It means -> {meaning}")

