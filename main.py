from pymorphy2 import MorphAnalyzer
from striprtf.striprtf import rtf_to_text


def read_txt_file_utf8():
    words = []
    file = open("text.txt", "r", encoding="utf-8")
    for line in file:
        words.append(line)
    file.close()
    return words


def read_rtf_file(file_name):
    with open(file_name + ".rtf") as infile:
        content = infile.read()
        text = rtf_to_text(content)
    return text


def word_frequency_in_text(words):
    frequency = {}
    for word in words:
        if word in frequency:
            frequency[word] += 1
        else:
            frequency[word] = 1
    return frequency


def sort_words_by_alphabet(words):
    return sorted(words)


def normal_form_of_word(word):
    morph = MorphAnalyzer()
    return morph.parse(word)[0].normal_form


def divide_text_on_words(text):
    return text.split("\n")


def delete_unnecessary_symbols(text):
    words = []
    for word in text:
        new_word = word.replace("\n", "")
        words.append(new_word)
    return words


def string_to_list(text):
    return text.split()


if __name__ == '__main__':
    text = read_txt_file_utf8()
    words = delete_unnecessary_symbols(text)
    frequency = word_frequency_in_text(words)
