from filter.filter import BadWordsFilter
from rasaInterface import RasaInterface

class ConversationEngine():
    def __init__(self) -> None:
        self.badWordsDetector = BadWordsFilter("filter/GoogleNews-vectors-negative300.bin")

    def cleanSentence(self, sent):
        if sent and sent[0] == ' ':
            return sent[1:]
        else:
            return sent
    

    def __call__(self, userInput:str, verbose:bool=False) -> str:
        userInput = self.cleanSentence(userInput)
        is_bad, bw = self.badWordsDetector.processSentence(userInput)

        userInput = "[BADWORD]" if is_bad else userInput

        answ = RasaInterface.interact(userInput)
        if answ is None:
            answ = "I didn't understand what you said, can you repeat again?"

        if verbose:
            print(f"{userInput=}\n{answ=}\n")
        
        return answ
    
    def formCompleted(self, sentence):
        # TODO: very dirty way, find something more elegant
        return "I'm currently analyzing all the possibilities to find the best dorm for you" in sentence

    def shortAnswerExpected(self, sentence):
        # TODO: even more dirty
        return "?" in sentence
    
    def earlyEnd(self, sentence):
        return "Bye" in sentence