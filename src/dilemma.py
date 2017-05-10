#!/usr/bin/env python2

import random
import os

from psychopy import visual, data

class DilemmaHandler(data.TrialHandler):
    def __init__(self, file, dilemmata):
        dilemmata = random.sample(data.importConditions(file), dilemmata)

        # Check if the loaded data matches the format.
        if len(dilemmata[0]) > 1 and 'id' in dilemmata[0] and 'text' in dilemmata[0]:
            data.TrialHandler.__init__(self, dilemmata, nReps=1, dataTypes=['order', 'id', 'primed', 'rating'])
        else:
            raise ValueError('Invalid prime list')
            
    def currentDilemma(self):
        return Dilemma(self.thisTrial['text'])
    
    def addResult(self, was_primed, rating):
        self.addData('order', self.thisIndex)
        self.addData('id', self.thisTrial['id'])
        self.addData('primed', was_primed)
        self.addData('rating', rating)
        
class Dilemma:
    def __init__(self, text):
        self.__text = text
        
    def text(self):
        return self.__text
        
    def show(self, win):
        text = visual.TextStim(win, self.__text, pos=(0, 0.2), height=0.06)
        rating = visual.RatingScale(win, high=10, labels=['Absolut unakzeptabel', 'Absolut akzeptabel'], scale=None, pos=(0, -0.5), acceptPreText='Bitte bewerten Sie die Entscheidung', acceptSize=2.8)
        #rating = visual.RatingScale(win, acceptText=['Ich stimme voll zu', 'Ich stimme zu', 'Ich stimme groesstenteils zu', 'Ich stimme eher zu', 'Ich stimme tendenziell zu', 'Ich stimme tendenziell nicht zu', 'Ich stimme eher nicht zu', 'Ich stimme groesstenteils nicht zu', 'Ich stimme nicht zu', 'Ich stimme ganz und gar nicht zu'], scale=None, pos=(0, -0.5), acceptPreText='Bitte bewerten Sie die Entscheidung', acceptSize=2.8)
        while rating.noResponse:
            text.draw()
            rating.draw()
            win.flip()
        return rating.getRating()