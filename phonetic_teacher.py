"""
phonetic alphabet teacher

Data from
http://www.military.com/join-armed-forces/guide-to-the-military-phonetic-alphabet.html

TODO:
    * add multiple spellings to take care of the alfa/alpha or juliett/juliette
      problem
"""

import os
import csv
import random
import speech_recognition as sr

class Color:
    PURPLE = '\033[95m'
    CYAN = '\033[36m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[34m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    RED = '\033[31m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def color_me(text, style='RED'):
    return getattr(Color, style) + text + Color.END

def say_answer(recog):
    """Retrieve the text for a spoken answer"""
    GAPIKEY = None
    try:
        with sr.Microphone() as source:
            print("Say your answer\n")
            audio = recog.listen(source, phrase_time_limit=20)
        return recog.recognize_google(audio, key=GAPIKEY)
    except sr.UnknownValueError:
        print('Speech recognition could not understand audio')
        raise sr.UnknownValueError
    except sr.RequestError as e:
        print('Could not request results from the speech recognition '
              'service; {0}'.format(e))
        raise sr.RequestError(e)

lookup = dict()
with open('alphabet.csv', 'r') as f:
    for idx, line in enumerate(csv.reader(f)):
        if idx == 0: 
            continue
        lookup[line[0]] = line[1]

words = list()
with open('words.csv', 'r') as f:
    words = f.read()
    words = [w.strip() for w in words.split('\n') if w != '']

r = sr.Recognizer() 

while True:
    curr_word = random.choice(words)

    try:
        accept = False
        while not accept:
            print('Say `{}`'.format(color_me(curr_word)))
            resp = say_answer(r)
            print('Your response was: `{}`'.format(color_me(resp,
                                                            style='BLUE')))
            ans = (input('Accept? [y]/n') or 'y')
            accept = (ans == 'y')
    except Exception as err:
        print('Err: {}'.format(err))
        print('Spoken responses not supported. Type it instead:\n')
        resp = input(curr_word + '\n')

    correct_ans = ' '.join([lookup[l] for l in curr_word.lower()
                            if l in lookup])
    if correct_ans == resp.lower():
        print("CONGRATS!")
    else:
        print('Incorrect.\n'
              'You entered:\t `{0}`,\n'
              'Correct Ans:\t `{1}`.\n'.format(resp,
                                               correct_ans))
        resp_words = resp.lower().split(' ')
        correct_ans_words = correct_ans.split(' ')
        n_corr_words = len(correct_ans_words)
        for idx, w in enumerate(resp_words):
            if idx == n_corr_words - 1:
                break
            if w != correct_ans_words[idx]:
                print('You seem to have missed {l}: {w}'.format(
                    l=correct_ans_words[idx],
                    w=lookup.get(w[0], 'Not a valid word')))
