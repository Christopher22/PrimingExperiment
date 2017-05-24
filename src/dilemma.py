#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import os

from psychopy import visual, data


class DilemmaHandler(data.TrialHandler):
    ''' A handler for multiple dilemmata. '''

    def __init__(self, file, dilemmata):
        '''
        Creates a new DilemmaHandler.
        :param str file: The path of the config file.
        :param number dilemmata: The number of dilemmata which is to be shown.
        :raises ValueError: If the path is not valid file.
        '''
        dilemmata = random.sample(data.importConditions(file), dilemmata)

        # Check if the loaded data matches the format.
        if len(dilemmata[0]) == 1 and 'dilemma' in dilemmata[0]:
            data.TrialHandler.__init__(self, dilemmata, nReps=1, dataTypes=['rating'], method="fullRandom")
        else:
            raise ValueError('Invalid prime list')

    def currentDilemma(self):
        '''
        Returns the current dilemma.
        :return Dilemma: The current Prime
        '''
        return Dilemma(self.thisTrial['dilemma'])

    def addResult(self, experiment, rating):
        '''
        Adds the result of a trial.
        :param ExperimentHandler experiment: The running experiment.
        :param number rating: The result of the trail.
        '''
        self.addData('rating', rating)
        experiment.nextEntry()


class Dilemma:
    ''' A dilemma. '''

    def __init__(self, text):
        '''
        Creates a new Dilemma.
        :param str text: The text of the dilemma.
        '''
        self.__text = text

    def text(self):
        '''
        Returns the text of the dilemma.
        :return str: The text of the dilemma.
        '''
        return self.__text

    def show(self, win):
        '''
        Shows a dilemma.
        :param visual.Window win: The text of the dilemma.
        '''
        text = visual.TextStim(win, self.__text, pos=(0, 0.2), height=0.06)
        rating = visual.RatingScale(
            win,
            low=0,
            high=9,
            labels=['Absolut unakzeptabel', 'Absolut akzeptabel'],
            scale=None,
            pos=(0, -0.5),
            acceptKeys=['space'],
            acceptPreText='Bitte bewerte die Entscheidung.',
            acceptSize=2.8,
            showValue=False,
            acceptText='Bewertung abgeben'
            )

        while rating.noResponse:
            text.draw()
            rating.draw()
            win.flip()
        return rating.getRating()
