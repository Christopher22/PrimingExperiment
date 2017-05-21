#!/usr/bin/python
# -*- coding: utf-8 -*-

from psychopy import visual

import random

def showRatings(window, title, ratings, buttonText, randomOrder=False):
    '''
    Present up to 4 rating scales.
    :param visual.Window window: The window to draw into.
    :param str title: The overall title.
    :param list ratings: [[name, [scale], title, numberSelection], ...]
    :param list buttonText: [buttonBefore, buttonAfter].
    :param bool randomOrder: Check if the order should be randomized.
    :return map: A map with the corresponding names and values.
    '''

    if len(buttonText) is not 2:
        raise ValueError('Invalid button texts')
    elif len(ratings) > 4:
        raise ValueError('Too much scales')

    # Shuffles the order if required
    if randomOrder:
        random.shuffle(ratings)

    # Create the overall title
    text = visual.TextStim(window, title, pos=(0, 0.75), height=0.075)

    # Create the rating scales
    ratingScales = []
    yPos = 0.45
    for i, scale in enumerate(ratings):
        ratingScale = visual.RatingScale(window, textSize=0.8, size=0.9, high=ratings[i][3], labels=ratings[i][1], scale=ratings[i][2], showAccept=(True if i == len(ratings) - 1 else False), pos=(0, yPos), acceptPreText=buttonText[0], acceptSize=2.8, showValue=False, acceptText=buttonText[1])
        ratingScales.append(ratingScale)
        yPos -= 0.35

    # Draw the scales
    while True:
        text.draw()

        # Check if all scales but the last are filled
        shouldEnd = True
        for ratingScale in ratingScales[:(len(ratingScales) - 1)]:
            ratingScale.draw()
            if shouldEnd is True and ratingScale.getRating() is None:
                shouldEnd = False

        # Exit if the last scales is filled, too
        if shouldEnd is True and not ratingScales[len(ratingScales) - 1].noResponse:
            break

        ratingScales[len(ratingScales) - 1].draw()
        window.flip()

    # Creates the result
    result = {}
    for i, scale in enumerate(ratingScales):
        result[ratings[i][0]] = scale.getRating()
    return result
