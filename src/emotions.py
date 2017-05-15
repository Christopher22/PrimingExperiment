#!/usr/bin/python
# -*- coding: utf-8 -*-

from psychopy import visual

import random

class Emotions:
    ''' A four-dimensional emotional collection of a subject. '''

    def __init__(self, happiness, anger, sadness, disgust):
        '''
        Creates a new emotion collection.
        :param number happiness: The happiness value on a scale between 0 and 10.
        :param number anger: The anger value on a scale between 0 and 10.
        :param number sadness: The sadness value on a scale between 0 and 10.
        :param number disgust: The disgust value on a scale between 0 and 10.
        '''
        self._happiness = happiness
        self._anger = anger
        self._sadness = sadness
        self._disgust = disgust

    def happiness(self):
        '''
        Returns the factor of happiness.
        :return number: A value between 0 and 10.
        '''
        return self._happiness

    def anger(self):
        '''
        Returns the factor of anger.
        :return number: A value between 0 and 10.
        '''
        return self._anger

    def sadness(self):
        '''
        Returns the factor of sadness.
        :return number: A value between 0 and 10.
        '''
        return self._sadness

    def disgust(self):
        '''
        Returns the factor of disgust.
        :return number: A value between 0 and 10.
        '''
        return self._disgust

    def save(self, exp):
        '''
        Save emotions into a running experiment.
        :param ExperimentHandler exp: The running experiment.
        '''
        exp.addData('happiness', self._happiness)
        exp.addData('anger', self._anger)
        exp.addData('sadness', self._sadness)
        exp.addData('disgust', self._disgust)
        exp.nextEntry()

    @staticmethod
    def from_window(window):
        '''
        Loads the collection from a questionaire showed in a window.
        :param visual.Window window: The window in which the questionaire should be drawn.
        :return Emotions: The collection.
        '''
        emotions = {
            'happiness': [u'Gar nicht fröhlich', u'Sehr fröhlich'],
            'anger': [u'Gar nicht wütend', u'Sehr wütend'],
            'sadness': [u'Gar nicht traurig', 'Sehr traurig'],
            'disgust': [u'Gar nicht angewidert', 'Sehr angewidert']
        }

        # Create a random order of the emotions
        emotionOrder = emotions.keys()
        random.shuffle(emotionOrder)

        # Create the explaining text
        text = stim = visual.TextStim(window, 'Bitte bewerten Sie ihre aktuellen Emotionen:', pos=(0, 0.75))

        # Generate rating scales dynamic
        yPos = 0.45
        for i in range(4):
            emotions[emotionOrder[i]] = visual.RatingScale(window, high=10, labels=emotions[emotionOrder[i]], scale=None, showAccept=(False if i < 3 else True), pos=(0, yPos), acceptPreText="Bitte bewerten Sie ihre Emotionen.", acceptSize=2.8, showValue=False, acceptText="Bewertung abgeben")
            yPos -= 0.3

        # Wait until all scales are filled
        while emotions[emotionOrder[3]].noResponse or emotions[emotionOrder[2]].getRating() is None or emotions[emotionOrder[1]].getRating() is None or emotions[emotionOrder[0]].getRating() is None:
            text.draw()
            for emotion in emotionOrder:
                emotions[emotion].draw()
            window.flip()

        return Emotions(emotions['happiness'].getRating(), emotions['anger'].getRating(), emotions['sadness'].getRating(), emotions['disgust'].getRating())
