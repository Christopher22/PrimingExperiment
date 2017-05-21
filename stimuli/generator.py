#!/usr/bin/env python3

# This script generates an appropriated primes.csv for the experiment.
# Usage: python generator.py > primes.csv

import glob
import re
import random

regex = re.compile('.*([A|B])([F|M])(\d+)NESGREY\.JPG$')
noise = ["noise01.png", "noise02.png", "noise03.png", "noise04.png"]

# Print the header
print('forward,prime,backward,neutral')

# Search all neutral faces
for path in glob.iglob('./faces/*NESGREY.JPG'):
    f = regex.match(path)
    if f:
        masks = random.sample(noise, 2)
        gender = f.group(2)
        neutral = 'faces/{}{}{}NESGREY.JPG'.format(f.group(1), gender, f.group(3))
        prime = 'faces/{}{}{}DISGREY.JPG'.format(f.group(1), gender, f.group(3))

        # Print the current row
        print('noise/{},{},noise/{},{}'.format(masks[0], prime, masks[1], neutral))
