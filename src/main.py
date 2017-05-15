#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from psychopy import visual, event, data

from stimuli import PrimeHandler
from dilemma import DilemmaHandler
from subject import Subject
from emotions import Emotions

from itertools import islice

def show_dilemmata(experiment, window, number_dilemmata, number_primes, forward, prime, backward, neutral):
    '''
    Shows a number of possible primed dilemmata.
    :param data.ExperimentHandler experiment: The current experiment
    :param number window: The number the stimuli are to be shown.
    :param str number_dilemmata: The number of dilemmata which are to be shown.
    :param number number_primes: The number of primes per dilemma which are to be shown.
    :param number forward: The number of frames the forward mask will be presented.
    :param number prime: The number of frames the priem will be presented.
    :param number backward: The number of frames the backward mask will be presented.
    :param number neutral:  The number of frames the neutral stimuli will be presented.
    '''
    dilemmata = DilemmaHandler('../stimuli/dilemmata.csv', number_dilemmata)
    primes = PrimeHandler('../stimuli/primes.csv', number_dilemmata * number_primes)

    experiment.addLoop(dilemmata)
    experiment.addLoop(primes)

    # Iterate through dilemmata.
    for _ in dilemmata:
        # Show the primes
        for _ in islice(primes, number_primes):
            result = primes.currentPrime().show(window, forward, prime, backward, neutral)
            primes.addResult(experiment, result)

        dilemma = dilemmata.currentDilemma()
        dilemmata.addResult(experiment, dilemma.show(window))

# Load the subject from the dialog
subject = Subject.from_dialog()
if subject:
    fileName = '../data/{}'.format(str(subject))
    exp = data.ExperimentHandler(name='PrimingMeetsDilemma', version='0.1', extraInfo=subject.to_dictionary(), originPath='../data/', savePickle=False, saveWideText=True, dataFileName=fileName)
    win = visual.Window(fullscr=True, monitor='testMonitor', checkTiming=True)

    # Print the length of a frame
    print("Prime length", win.monitorFramePeriod)

    show_dilemmata(exp, win, number_dilemmata=1, number_primes=3, forward=1, prime=1, backward=1, neutral=157)

    # Check emotions afterward
    emotion = Emotions.from_window(win)
    emotion.save(exp)

    win.close()
