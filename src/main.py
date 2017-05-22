#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from psychopy import visual, event, data
from psychopy.constants import PLAYING

from stimuli import PrimeHandler
from dilemma import DilemmaHandler
from subject import Subject
from emotions import Emotions
from dsr import DSR

from itertools import islice

def show_dilemmata(experiment, window, dilemmata, number_dilemmata, number_primes, forward, prime, backward, neutral):
    '''
    Shows a number of possible primed dilemmata.
    :param data.ExperimentHandler experiment: The current experiment
    :param visual.Window window: The window to draw into.
    :param number dilemmata: The file from which the dilemmata should be loaded.
    :param str number_dilemmata: The number of dilemmata which are to be shown.
    :param number number_primes: The number of primes per dilemma which are to be shown.
    :param number forward: The number of frames the forward mask will be presented.
    :param number prime: The number of frames the priem will be presented.
    :param number backward: The number of frames the backward mask will be presented.
    :param number neutral:  The number of frames the neutral stimuli will be presented.
    '''
    dilemmata = DilemmaHandler(dilemmata, number_dilemmata)
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

def show_movie(win):
    '''
    Presents a movie for the de-priming.
    :param visual.Window win: The window to draw into.
    '''
    text = visual.TextStim(win, "Eine kleine Pause...", pos=(0, 0.8))
    mov = visual.MovieStim3(win, '../stimuli/pause.mp4', size=(640, 480))
    mov.play()
    while mov.status == PLAYING:
        text.draw()
        mov.draw()
        win.flip()

# Load the subject from the dialog
subject = Subject.from_dialog()
if subject:
    fileName = '../data/{}'.format(str(subject))
    exp = data.ExperimentHandler(name='PrimingMeetsDilemma', version='0.1', extraInfo=subject.to_dictionary(), originPath='../data/', savePickle=False, saveWideText=True, dataFileName=fileName)
    win = visual.Window(fullscr=True, monitor='testMonitor', checkTiming=True)

    # Show first dilemmata group
    show_dilemmata(exp, win, '../stimuli/dilemmata0.csv', number_dilemmata=10, number_primes=7, forward=1, prime=(1 if subject.group() is "A" else 0), backward=1, neutral=237)
    Emotions.from_window(win).save(exp)

    # Show depriming sequence
    #show_movie(win)
    #Emotions.from_window(win).save(exp)

    # Show second dilemmata group
    show_dilemmata(exp, win, '../stimuli/dilemmata1.csv', number_dilemmata=10, number_primes=7, forward=1, prime=(0 if subject.group() is "A" else 1), backward=1, neutral=237)
    Emotions.from_window(win).save(exp)

    # Check disgust level
    DSR.from_window(win).save(exp)

    win.close()
