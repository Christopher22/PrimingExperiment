#!/usr/bin/env python2

import random
import os

from psychopy import visual, data, event

class PrimeHandler(data.TrialHandler):
    ''' A handler for multiple primes loaded from a file. '''

    def __init__(self, file, primes):
        '''
        Creates a new PrimeHandler.
        :param str file: The path of the config file.
        :param number primes: The number of primes which is to be shown.
        :raises ValueError: If the paths are not valid files.
        '''
        primes = random.sample(data.importConditions(file), primes)

        # Check if the loaded data matches the format.
        if len(primes[0]) >= 6 and 'id' in primes[0] and 'forward' in primes[0] and 'prime' in primes[0] and 'backward' in primes[0] and 'neutral' in primes[0] and 'gender' in primes[0]:
            self.__basepath = os.path.dirname(os.path.abspath(file))
            data.TrialHandler.__init__(self, primes, nReps=1, dataTypes=['order', 'id', 'correct'])
        else:
            raise ValueError('Invalid prime list')

    def currentPrime(self):
        '''
        Returns the current prime.
        :return Prime: The current Prime
        '''
        # Convert local paths to global paths
        forward_path = os.path.join(self.__basepath, self.thisTrial['forward'])
        prime_path = os.path.join(self.__basepath, self.thisTrial['prime'])
        backward_path = os.path.join(self.__basepath, self.thisTrial['backward'])
        neutral_path = os.path.join(self.__basepath, self.thisTrial['neutral'])
        return Prime(self.thisTrial['id'], forward_path, prime_path, backward_path, neutral_path)

    def addResult(self, gender_choice):
        '''
        Adds the result of a priming session.
        '''
        self.addData('order', self.thisIndex)
        self.addData('id', self.thisTrial['id'])
        self.addData('correct', self.thisTrial['gender'] == gender_choice)

class Prime:
    ''' A drawable prime. '''

    def __init__(self, id, forward_path, prime_path, backward_path, neutral_path):
        '''
        Creates a new prime.
        :param number id: An id for the prime.
        :param str neutral_path: The path of the image which is the forward and backward mask.
        :param str prime_path: The path of the image which is the actual prime.
        :raises ValueError: If the paths are not valid files.
        '''
        self.id = id
        if not os.path.isfile(forward_path):
            raise ValueError('Forward path invalid!')
        elif not os.path.isfile(backward_path):
            raise ValueError('Backward path invalid!')
        elif not os.path.isfile(prime_path):
            raise ValueError('Prime path invalid!')
        elif not os.path.isfile(neutral_path):
            raise ValueError('Neutral path invalid!')
        else:
            self._forward = forward_path
            self._backward = backward_path
            self._prime = prime_path
            self._neutral = neutral_path

    def prime(self, window):
        '''
        Returns the drawable prime.
        :param visual.Window window: The window in which the prime should be drawn.
        :return: Drawable prime.
        '''
        return visual.ImageStim(window, self._prime)

    def forward_mask(self, window):
        '''
        Returns the drawable forward mask.
        :param visual.Window window: The window in which the prime should be drawn.
        :return: Drawable forward mask.
        '''
        return visual.ImageStim(window, self._forward)

    def backward_mask(self, window):
        '''
        Returns the drawable forward mask.
        :param visual.Window window: The window in which the prime should be drawn.
        :return: Drawable forward mask.
        '''
        return visual.ImageStim(window, self._backward)
        
    def neutral(self, window):
        '''
        Returns the drawable backward mask.
        :param visual.Window window: The window in which the prime should be drawn.
        :return: Drawable forward mask.
        '''
        return visual.ImageStim(window, self._neutral)

    def show(self, window, forward_len, prime_len, backward_len, neutral_len):
        forward = self.forward_mask(window)
        backward = self.backward_mask(window)
        prime = self.prime(window)
        neutral = self.neutral(window)

        # Predraw all stimuli for performance reasons
        forward.draw()
        backward.draw()
        prime.draw()
        neutral.draw()

        for frame in range(forward_len):
            forward.draw()
            window.flip()
            
        for frame in range(prime_len):
            prime.draw()
            window.flip()
        
        for frame in range(backward_len):
            backward.draw()
            window.flip()
            
        for frame in range(neutral_len):
            neutral.draw()
            window.flip()

        visual.TextStim(window, 'Welches Geschlecht hatte die gerade gezeigte Person? Bitte druecke "f" im Falle einer Frau oder "m" im Falle eines Mannes.').draw()
        window.flip()

        return event.waitKeys(keyList=['f', 'm'])[0]
