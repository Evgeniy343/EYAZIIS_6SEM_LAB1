from tkinter.filedialog import askopenfilename

from striprtf.striprtf import rtf_to_text

from TextWorkingMechanism import word_frequency_in_text, create_vocabulary


def read_rtf_file(file_name):
    with open(file_name) as infile:
        content = infile.read()
        text = rtf_to_text(content)
    return text


def extract_words_from_rtf_file(file_name):
    text = read_rtf_file(file_name)
    words = text.split()
    words = sorted(words)
    frequency = word_frequency_in_text(words)
    create_vocabulary(words, frequency)


def open_rtf_file():
    file_name = askopenfilename(filetypes=[("RTF files", "*.rtf")],
                                defaultextension=".rtf")
    if file_name is None:
        return
    elif file_name.endswith(".rtf"):
        extract_words_from_rtf_file(file_name)
    else:
        return


