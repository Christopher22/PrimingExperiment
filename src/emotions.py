#!/usr/bin/python
# -*- coding: utf-8 -*-

from psychopy import visual
from helper import showRatings

import numbers

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
        if not all(isinstance(emotion, numbers.Number) and emotion >= 0 and emotion < 11 for emotion in [happiness, anger, sadness, disgust]):
            raise ValueError("Invalid range")

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
        results = showRatings(window, "Bitte bewerten Sie ihre aktuellen Emotionen:", [
            ['happiness', [u'Gar nicht fröhlich', u'Sehr fröhlich'], u'Fröhlichkeit', 10],
            ['anger', [u'Gar nicht wütend', u'Sehr wütend'], 'Wut', 10],
            ['sadness', [u'Gar nicht traurig', 'Sehr traurig'], 'Traurigkeit', 10],
            ['disgust', [u'Gar nicht angewidert', 'Sehr angewidert'], 'Ekel', 10]
        ], ["Bitte bewerten Sie ihre Emotionen.", "Bewertung abgeben"], True)

        return Emotions(results['happiness'], results['anger'], results['sadness'], results['disgust'])
