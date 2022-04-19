from tkinter.filedialog import askopenfilename

from TextWorkingMechanism import word_frequency_in_text, create_vocabulary


def read_txt_file_utf8(file_name):
    words = []
    file = open(file_name, "r", encoding="utf-8")
    for line in file:
        words.append(line)
    file.close()
    return words


def divide_text_into_words(text):
    words = []
    for line in text:
        for word in line.split():
            words.append(word)
    return words


def extract_words_from_txt_file(file_name):
    text = read_txt_file_utf8(file_name)
    words = divide_text_into_words(text)
    frequency = word_frequency_in_text(words)
    create_vocabulary(words, frequency)


def open_txt_file():
    file_name = askopenfilename(filetypes=[("TXT files", "*.txt")],
                                defaultextension=".txt")
    if file_name is None:
        return
    elif file_name.endswith(".txt"):
        extract_words_from_txt_file(file_name)
    else:
        return
