#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from psychopy import visual, event

import stimuli
import dilemma

def show_primes(win):
    primes = stimuli.PrimeHandler('../stimuli/stimuli.csv', 3)
    for _ in primes:
        result = primes.currentPrime().show(win, 3, 1, 5, 115)
        primes.addResult(result)
    return primes

win = visual.Window(fullscr=True, monitor='testMonitor', checkTiming=True)
print("Prime length", win.monitorFramePeriod)

dilemmata = dilemma.DilemmaHandler('../stimuli/dilemmata.csv', 1)
for _ in dilemmata:
    prime_data = show_primes(win)
    dilemma = dilemmata.currentDilemma()
    dilemmata.addResult(True, dilemma.show(win))

win.close()
