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
        if len(primes[0]) == 4 and 'forward' in primes[0] and 'prime' in primes[0] and 'backward' in primes[0] and 'neutral' in primes[0]:
            self.__basepath = os.path.dirname(os.path.abspath(file))
            data.TrialHandler.__init__(self, primes, nReps=1, dataTypes=['order', 'correct'])
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
        return Prime(forward_path, prime_path, backward_path, neutral_path)

    def addResult(self, experiment, result):
        '''
        Adds the result of a priming session.
        '''
        self.addData('result', result)
        experiment.nextEntry()

class Prime:
    ''' A drawable prime. '''

    def __init__(self, forward_path, prime_path, backward_path, neutral_path):
        '''
        Creates a new prime.
        :param number id: An id for the prime.
        :param str forward_path: The path of the image which is the forward mask.
        :param str neutral_path: The path of the image which is the neutral stimulus.
        :param str prime_path: The path of the image which is the actual prime.
        :param str backward_path: The path of the image which is the backward mask.
        :raises ValueError: If the paths are not valid files.
        '''
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
        '''
        Shows a prime
        :param visual.Window window: The window in which the prime should be drawn.
        :param number forward_len: The lenght of the forward mask in frames.
        :param number prime_len: The lenght of the prime in frames.
        :param number backward_len: The lenght of the backward mask in frames.
        :param number neutral_len: The lenght of the neutral image in frames.
        :return: A result of an attractiveness test.
        '''
        forward = self.forward_mask(window)
        backward = self.backward_mask(window)
        prime = self.prime(window)
        neutral = self.neutral(window)

        # Predraw all stimuli for performance reasons
        forward.draw()
        backward.draw()
        prime.draw()
        neutral.draw()

        # Draw the forward mask.
        for frame in range(forward_len):
            forward.draw()
            window.flip()

        # Draw the prime.
        for frame in range(prime_len):
            prime.draw()
            window.flip()

        # Draw the backward mask.
        for frame in range(backward_len):
            backward.draw()
            window.flip()

        # Draw the neutral image.
        for frame in range(neutral_len):
            neutral.draw()
            window.flip()
            if event.getKeys('space'):
                break

        # Remove unecessary spaces
        event.clearEvents()

        rating = visual.RatingScale(window, high=10, acceptKeys=['space'], labels=['Absolut unsympathisch', 'Absolut sympathisch'], scale=None, pos=(0,0), acceptPreText='Bitte bewerten Sie das Aussehen.', showValue=False, acceptSize=2.8, acceptText='Bewertung abgeben')
        while rating.noResponse:
            rating.draw()
            window.flip()
        return rating.getRating()
