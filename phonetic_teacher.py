"""Phonetic alphabet teacher

Data from
http://www.military.com/join-armed-forces/guide-to-the-military-phonetic-alphabet.html
"""
import os
import csv
import random
import speech_recognition as sr


def color_me(text, style='RED'):
    """give back text according to the color in `style`"""
    color = {
        'PURPLE': '\033[95m',
        'CYAN': '\033[36m',
        'DARKCYAN': '\033[36m',
        'BLUE': '\033[34m',
        'GREEN': '\033[32m',
        'YELLOW': '\033[33m',
        'RED': '\033[31m',
        'BOLD': '\033[1m',
        'UNDERLINE': '\033[4m',
        'END': '\033[0m'
        }
    return '{color}{text}{ending}'.format(color=color.get(style, 'RED'),
                                          text=text,
                                          ending=color['END'])


def say_answer(recog):
    """Retrieve the text for a spoken answer"""
    try:
        with sr.Microphone() as source:
            print("Say your answer\n")
            audio = recog.listen(source, phrase_time_limit=20)
        return recog.recognize_google(audio)
    except sr.UnknownValueError:
        print('Speech recognition could not understand audio')
        raise sr.UnknownValueError
    except sr.RequestError as err:
        print('Could not request results from the speech recognition '
              'service; {0}'.format(err))
        raise sr.RequestError(err)


def get_dictionary(filename):
    """text file is formatted like:
     letter,answer,alternate_spelling1,alternate_spelling2
     letter,answer
     letter,answer,alternate_spelling1
    output:
      {'a': ('alpha', 'alfa',),
       'b': ('bravo',),
       ...
    """
    lookup = dict()
    with open(filename, 'r') as alpha_file:
        for idx, line in enumerate(csv.reader(alpha_file)):
            if idx == 0:
                continue
            lookup[line[0]] = tuple(line[1:])
    return lookup


def get_words(wordset='animals'):
    """Retrieve a sample of words from a file.
    Format:
        word1
        word2
        word3
        ...
    Output:
        ['word1', 'word2', 'word3', ...]
    """
    curr_dir = os.path.dirname(__file__)
    file_loc = 'wordsets/{wordset}.csv'.format(wordset=wordset)
    with open(os.path.join(curr_dir, file_loc), 'r') as word_file:
        words = word_file.read()
    return [w.strip() for w in words.split('\n') if w != '']


def transform_ans(ans):
    """take a response string, convert it to a list with all
    lower case values
    """
    temp = ans.split(' ')
    return [a.strip().lower() for a in temp
            if a.strip() != '']


def is_correct(resp, ans):
    """Tells whether the user entered the correct answer
    Args:
        resp (list of str): User response as a list of text
        ans (list of tuples of str): List of words that are acceptable answers
    Returns:
        bool: whether `resp` is equal to the possible answers in `ans`
    """
    num_correct = sum([a in ans[idx]
                       for idx, a in enumerate(resp)])
    return num_correct == len(ans)


def print_ans(ans):
    """print correct answer vertically
    Args:
        ans (list of tuples of strings)
    """
    return '\n'.join([color_me(w[0][0].upper(), style='BLUE') + w[0][1:]
                      for w in ans])


def main():
    """main operation"""
    lookup = get_dictionary('alphabet.csv')
    words = get_words(wordset='animals')
    recog = sr.Recognizer()

    while True:
        curr_word = random.choice(words)
        try:
            accept = False
            while not accept:
                raise sr.UnknownValueError
                print('Say `{}`'.format(color_me(curr_word)))
                resp = say_answer(recog)
                print('Your response was: `{}`'.format(color_me(resp,
                                                                style='BLUE')))
                ans = (input('Accept? [y]/n') or 'y')
                accept = (ans == 'y')
        except (sr.UnknownValueError, sr.RequestError) as err:
            print('Spoken responses not supported {}. '
                  'Type it instead:\n'.format(err))
            resp = input(color_me(curr_word) + '\n')

        trans_ans = transform_ans(resp)
        correct_ans = [lookup[l] for l in curr_word.lower()
                       if l in lookup]
        if is_correct(trans_ans, correct_ans):
            print("CONGRATS!")
        else:
            print('{incorrect}\n'
                  '{answer}\n'
                  'You entered:\t `{resp}`,\n'.format(
                      incorrect=color_me('Incorrect'),
                      answer=print_ans(correct_ans),
                      resp=resp))


if __name__ == '__main__':
    main()
