from psychopy import gui

import hashlib
import base64
import time

class Subject:
    ''' A participating subject. '''

    def __init__(self, id, group, age, gender):
        '''
        Creates a new subject.
        :param str id: The id of the subject.
        :param str age: The age of the subject.
        :param str gender: The gender of the subject ("m" or "f").
        '''
        self._id = id
        self._group = group
        self._age = age
        self._gender = gender

    def __str__(self):
        '''
        Returns a textual representation.
        :return str: The stringified subject.
        '''
        return self._id

    def id(self):
        '''
        Returns the id.
        :return str: The id.
        '''
        return self._id

    def group(self):
        '''
        Returns the group of the subject.
        :return str: The group of the object.
        '''
        return self._group

    def age(self):
        '''
        Returns the age of the subject.
        :return number: The age.
        '''
        return self._age

    def is_female(self):
        '''
        Returns if the subject is female.
        :return bool: True, if the subject is female.
        '''
        return self._gender == 'f'

    def to_dictionary(self):
        '''
        Returns a representation as dictionary.
        :return: A dictionary
        '''
        return {'id': self._id, 'groupt': self._group, 'age': self._age, 'gender': self._gender}

    @staticmethod
    def from_dialog():
        '''
        Loads the subject data from a GUI.
        :return Subject: The subject or False on error.
        '''
        def generate_id():
            '''
            Generates an unique id based on the current time.
            '''
            current_time = str(time.time() * 1000)
            hash_str = str(hashlib.pbkdf2_hmac('sha256', current_time, b'christopher', 100000, 32))
            return base64.b32encode(hash_str)[:10]

        dlg = gui.Dlg(title="Willkommen!", labelButtonOK='Starten', labelButtonCancel='Beenden')
        dlg.addText('Herzlich willkommen zu unserem Experiment!')
        dlg.addText('Bitte starte es erst, wenn du dazu aufgefordert wirst.')

        dlg.addFixedField("Anonyme ID:", generate_id())
        dlg.addField('Gruppe:', choices=["A", "B"])
        dlg.addField('Alter:')
        dlg.addField('Geschlecht:', choices=["Frau", "Mann"])

        dlg.show()
        if dlg.OK:
            id, group, age, gender = dlg.data
            if int(age) >= 18: return Subject(id, group, age, 'f' if gender == 'Frau' else 'm')

        return False
