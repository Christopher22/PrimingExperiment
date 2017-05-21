#!/usr/bin/python
# -*- coding: utf-8 -*-

from helper import showRatings

import numbers

class DSR:
    ''' A python class which implements "The DS-R (Haidt, McCauley & Rozin, 1994, modified by Olatunji et al. 2007)". '''

    def __init__(self, ratings):
        '''
        Creates a new instance of the test for a subject.
        :param list ratings: The ratings of the 27 questions in the range [0, 4].
        :raises ValueError: If the ratings was not valid.
        '''
        if len(ratings) is not 27 or not all(isinstance(rating, numbers.Number) and 0 <= rating <= 4 for rating in ratings):
            raise ValueError("Invalid ratings")

        ratings[0] = 4 - ratings[0]
        ratings[5] = 4 - ratings[5]
        ratings[9] = 4 - ratings[9]

        self._isReliable = True if ratings[11] >= 3 and ratings[15] <= 1 else False
        self._core = (ratings[0] + ratings[2] + ratings[5] + ratings[7] + ratings[10] + ratings[12] + ratings[14] + ratings[16] + ratings[19] + ratings[21] + ratings[24] + ratings[26]) / 12
        self._anrem = (ratings[1] + ratings[4] + ratings[6] + ratings[9] + ratings[13] + ratings[18] + ratings[20] + ratings[23]) / 8
        self._contam = (ratings[3] + ratings[8] + ratings[17] + ratings[22] + ratings[25]) / 5
        self._complete = (sum(ratings) - ratings[11] - ratings[15]) / 25

    def isReliable(self):
        '''
        Returns if the subject seems to be reliable depending on the catch-questions.
        :return bool: True, if subject is reliable.
        '''
        return self._isReliable

    def coreDisgust(self):
        '''
        Returns the core disgust.
        :return number: The rating of core disgust.
        '''
        return self._core

    def animalReminderDisgust(self):
        '''
        Returns the animal-reminder disgust.
        :return number: The rating of animal-reminder disgust.
        '''
        return self.__anrem

    def contaminationDisgust(self):
        '''
        Returns the contamination disgust.
        :return number: The rating of contamination disgust.
        '''
        return self._contam

    def overallDisgust(self):
        '''
        Returns the overall disgust.
        :return number: The rating of overall disgust.
        '''
        return self._complete

    def save(self, exp):
        '''
        Save disgust scales into a running experiment.
        :param ExperimentHandler exp: The running experiment.
        '''
        exp.addData('coreDisgust', self._core)
        exp.addData('animalReminderDisgust', self._anrem)
        exp.addData('contaminationDisgust', self._contam)
        exp.addData('overallDisgust', self._complete)
        exp.addData('isReliable', self._isReliable)
        exp.nextEntry()

    @staticmethod
    def from_window(window):
        '''
        Loads the DS-R from a questionaire showed in a window.
        :param visual.Window window: The window in which the questionaire should be drawn.
        :return Emotions: The DS-R.
        '''
        TITLE = "Bitte bewerten Sie folgende Aussagen:"
        SCALE = ["Ich stimme ganz und gar nicht zu", "Ich stimme voll und ganz zu"]
        BUTTONS = ["Bitte bewerten Sie ihre Emotionen.", "Bewertung abgeben"]

        results = showRatings(window, TITLE, [
            [0, SCALE, u'Ich wäre unter bestimmten Umständen dazu bereit Affenfleisch zu probieren.', 5],
            [1, SCALE, u'Es würde mich stören in einem Naturkundekurs eine in einem Glas preservierte, menschliche Hand zu sehen.', 5],
            [2, SCALE, u'Es macht mir etwas aus zu hören wie sich jemand mit Schleim im Hals räuspert.', 5],
            [3, SCALE, u'Ich lasse nie einen Teil meines Körpers den Toilettensitz einer öffentlichen Toilette berühren.', 5]
        ], BUTTONS, False)

        results.update(showRatings(window, TITLE, [
            [4, SCALE, u'Ich würde mich sehr darum bemühen es zu vermeiden durch einen Friedhof zu gehen.', 5],
            [5, SCALE, u'Eine Kakerlake bei jemanden Zuhause zu sehen stört mich nicht.', 5],
            [6, SCALE, u'Es würde mich ungemein stören, eine Leiche zu berühren.', 5],
            [7, SCALE, u'Wenn ich jemanden sich übergeben sehe, wird mir schlecht.', 5]
        ], BUTTONS, False))

        results.update(showRatings(window, TITLE, [
            [8, SCALE, u'Ich würde wahrscheinlich nicht zu meinem Lieblingsrestaurant gehen, wenn ich herausfände, dass der Koch eine Erkältung hat.', 5],
            [9, SCALE, u'Es würde mich überhaupt nicht stören, zuzusehen wie eine Person mit einem Glasauge das Auge aus der Fassung nimmt.', 5],
            [10, SCALE, u'Es würde mich stören eine Ratte über meinen Weg im Park rennen zu sehen.', 5],
            [11, SCALE, u'Ich würde eher ein Stückchen Obst, als ein Stückchen Papier essen.', 5]
        ], BUTTONS, False))

        results.update(showRatings(window, TITLE, [
            [12, SCALE, u'Selbst wenn ich hungrig wäre, würde ich nicht einen Teller meiner Lieblingssuppe essen, sollte diese zuvor mit einer gebrauchten, jedoch gründlich gereinigten Fliegenklatsche umgerührt worden sein.', 5],
            [13, SCALE, u'Es würde mir etwas ausmachen, in einem netten Hotelzimmer zu schlafen, wenn ich wüsste, dass ein Mann eine Nacht vorher in diesem Zimmer an einem Herzanfall gestorben ist.', 5]
        ], BUTTONS, False))

        SCALE = [u'Überhaupt nicht ekelig', 'Extrem ekelig']

        results.update(showRatings(window, TITLE, [
            [14, SCALE, u'Du siehst Maden auf einem Stück Fleisch, in einem Außenabfall-Eimer liegt.', 5],
            [15, SCALE, u'Du siehst eine Person, die einen Apfel mit Messer und Gabel isst.', 5],
            [16, SCALE, u'Während du durch einen Tunnel unter einer Eisenbahn-Spur hindurchgehst, riechst du Urin.', 5],
            [17, SCALE, u'Du nimmst einen Schluck von einem Getränk, und realisierst erst danach, dass du von einem Glas getrunken hast, aus dem ein Bekannter von dir schon getrunken hatte.', 5]
        ], BUTTONS, False))

        results.update(showRatings(window, TITLE, [
            [18, SCALE, u'Die Lieblingskatze deines Freunds stirbt, und du musst die Leiche mit deinen bloßen Händen aufsammeln.', 5],
            [19, SCALE, u'Du siehst, dass jemand Ketchup auf Vanille-Eiscreme verteilt, und es isst.', 5],
            [20, SCALE, u'Nach einem Unfall siehst du einen Man mit entblößten Gedärmen.', 5],
            [21, SCALE, u'Du findest heraus, dass ein Freund von dir seine Unterwäsche nur einmal in der Woche wechselt.', 5]
        ], BUTTONS, False))

        results.update(showRatings(window, TITLE, [
            [22, SCALE, u'Ein Freund bietet dir ein Stück Schokolade an, das wie Hundekacke geformt ist.', 5],
            [23, SCALE, u'Du berührst zufällig die Asche einer verbrannten Leiche.', 5],
            [24, SCALE, u'Du willst gerade von einem Glas Milch trinken, als du riechst, dass die Milch verdorben ist.', 5],
            [25, SCALE, u'Als Teil des Sexualunterrichtes wirst du gebeten, ein neues, ungeschmiertes Kondom mit dem Mund aufzublasen.', 5]
        ], BUTTONS, False))

        results.update(showRatings(window, TITLE, [
            [26, SCALE, u'Du gehst barfuß auf Beton spazieren und trittst auf einen Regenwurm.', 5]
        ], BUTTONS, False))

        result = []
        for i in range(27):
            result.append(results[i])
        return DSR(result)
