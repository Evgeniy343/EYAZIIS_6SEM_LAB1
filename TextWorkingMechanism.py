from pymorphy2 import MorphAnalyzer

from DataType import Word, main_dictionary


def create_vocabulary(words, frequency):
    for word in words:
        new_word = Word()
        new_word.lexeme = word
        new_word.normal_form = normal_form_of_word(word)
        new_word.frequency = frequency[word]
        main_dictionary.append(new_word)


def word_frequency_in_text(words):
    frequency = {}
    for word in words:
        if word in frequency:
            frequency[word] += 1
        else:
            frequency[word] = 1
    return frequency


def normal_form_of_word(word):
    morph = MorphAnalyzer()
    return morph.parse(word)[0].normal_form
