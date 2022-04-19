import tkinter.ttk as ttk
from tkinter import *
from tkinter import Tk, Label, Button, Entry, Frame, NO, W, WORD, Text
from tkinter import messagebox as mb
from tkinter.filedialog import asksaveasfile
from xml.dom import minidom

from DataType import main_dictionary
from RTFWorkingMechanism import open_rtf_file
from TXTWorkingMechanism import open_txt_file
from TextWorkingMechanism import create_vocabulary, word_frequency_in_text

HELPTEXT = '''                    
Программа предназначена для для обработки текстов на руском языке.
Здесь представлен функционал:
    1. Создание словаря из текста из файла расширения .txt
    2. Создание словаря из текста из файла расширения .rtf
    3. Создание словаря из текста поля ввода
    4. Удаление слова из словаря
    5. Отображение словаря в виде таблицы
    6. Очистка словаря
    7. Добавление морфологических данных к слову
'''


def update_vocabulary():
    vocabularyTree.delete(*vocabularyTree.get_children())
    repeated_words = [" "]
    repeated = 1
    for word in main_dictionary:
        for repeat_word in repeated_words:
            if word.lexeme == repeat_word:
                repeated = 0
                break
        if repeated == 1:
            vocabularyTree.insert('', 'end', values=(word.lexeme, word.normal_form, word.frequency, word.info))
        repeated_words.append(word.lexeme)
        repeated = 1


S


def push_table_from_txt_file():
    open_txt_file()
    update_vocabulary()


def push_table_from_rtf_file():
    open_rtf_file()
    update_vocabulary()


def clear_vocabulary():
    vocabularyTree.delete(*vocabularyTree.get_children())
    main_dictionary.clear()


def delete_item():
    try:
        selected = vocabularyTree.focus()
        temp = vocabularyTree.item(selected, 'values')

        for word in main_dictionary:
            if word.lexeme == temp[0]:
                main_dictionary.remove(word)

        vocabularyTree.delete(selected)
    except Exception:
        mb.showerror(title="Error", message="Have you selected any item before clicking that button?..")
        return


def create_vocabulary_from_text_field():
    main_dictionary.clear()
    text = inputText.get(1.0, END).replace('\n', '')
    words = text.split()
    words = sorted(words)
    frequency = word_frequency_in_text(words)
    create_vocabulary(words, frequency)
    update_vocabulary()


def changeInf():
    try:
        popup()
    except Exception:
        mb.showerror(title="Error", message="Have you selected any item before clicking that button?..")
        return


def popup():
    selected = vocabularyTree.focus()
    temp = vocabularyTree.item(selected, 'values')
    for pack in popupWindow.pack_slaves():
        pack.pack_forget()

    popupInputText.delete(0, "end")
    popupWindow.title("Alter")
    popupWindow.geometry("400x250")
    label = Label(popupWindow, text="Морфологическая информация слофовормы " + temp[0])
    if temp[3] == '':
        info = Label(popupWindow,
                     text="Никакой морофологической информации \nо данной словоформе в словаре ещё не представленно")
    else:
        info = Label(popupWindow, text=temp[3])
    label.pack()
    info.pack()
    alert = Label(popupWindow, text="Введите морфологическую информацию")
    buttonFrame = Frame(popupWindow, bd=2)
    button1 = Button(buttonFrame, text="Ввести", width=18, height=2)
    button2 = Button(buttonFrame, text="Назад", width=18, height=2)
    alert.pack()
    popupInputText.pack()
    buttonFrame.pack()
    button1.config(command=change_now)
    button2.config(command=popupWindow.withdraw)
    button1.pack(side='left')
    button2.pack(side='left')
    popupWindow.deiconify()
    popupWindow.mainloop()


def show_help():
    print(help)


def change_now():
    selected = vocabularyTree.focus()
    temp = vocabularyTree.item(selected, 'values')
    for word in main_dictionary:
        if word.lexeme == temp[0]:
            word.info = popupInputText.get()
    update_vocabulary()
    popupWindow.withdraw()


def show_help():
    mb.showinfo(title="Помощь", message=HELPTEXT)


def save_dictionary():
    file = asksaveasfile(filetypes=(("dict file", "*.dict"),), defaultextension=("dict file", "*.dict"))
    if file is None:
        return
    doc = minidom.Document()
    root_el = doc.createElement('root')

    words = main_dictionary

    words.sort(key=lambda x: x.lexeme, reverse=True)

    for i in words:
        word = doc.createElement('word')
        lexeme = doc.createElement('lexeme')
        normal_form = doc.createElement('normal_form')
        frequency = doc.createElement('frequency')
        info = doc.createElement('info')

        text1 = doc.createTextNode(i.lexeme)
        text2 = doc.createTextNode(i.normal_form)
        text3 = doc.createTextNode(str(i.frequency))

        lexeme.appendChild(text1)
        normal_form.appendChild(text2)
        frequency.appendChild(text3)
        for j in i.info:
            info.appendChild(doc.createTextNode(j))

        word.appendChild(lexeme)
        word.appendChild(normal_form)
        word.appendChild(frequency)
        word.appendChild(info)

        root_el.appendChild(word)
    doc.appendChild(root_el)

    xml_str = doc.toprettyxml(indent="  ", encoding='UTF-8')

    file.write(str(xml_str, 'UTF-8'))
    file.close()


if __name__ == '__main__':
    root = Tk()
    main_menu = Menu(root)
    main_menu.add_command(label='Сохранить имеющийся словарь в файл', command=save_dictionary)
    main_menu.add_command(label='Помощь', command=show_help)
    root.config(menu=main_menu)

    space0 = Label(root)
    inputFrame = Frame(root, bd=2)
    inputText = Text(inputFrame, height=10, width=130, wrap=WORD)
    space01 = Label(root)
    mainMenuFrame = Frame(root, bd=2)
    createVocabularyButton_textField = Button(mainMenuFrame, text='Создать словарь по тексту', width=30, height=2,
                                              bg='grey')

    createVocabularyButton_textFile_txt = Button(mainMenuFrame, text='Создать словарь из файла .txt', width=25,
                                                 height=2, bg='grey')
    createVocabularyButton_textFile_rtf = Button(mainMenuFrame, text='Создать словарь из текстового файла .rtf',
                                                 width=35,
                                                 height=2, bg='grey')

    space1 = Label(root)
    vocabularyFrame = Frame(root, bd=2)
    vocabularyTree = ttk.Treeview(vocabularyFrame,
                                  columns=("Словоформа", "Лексема", "Частота встречаемости слова", "Информация"),
                                  selectmode='browse', height=11)
    vocabularyTree.heading('Словоформа', text="Словоформа", anchor=W)
    vocabularyTree.heading('Лексема', text="Лексема", anchor=W)
    vocabularyTree.heading('Частота встречаемости слова', text="Частота встречаемости слова", anchor=W)
    vocabularyTree.heading('Информация', text="Информация", anchor=W)
    vocabularyTree.column('#0', stretch=NO, minwidth=0, width=0)
    vocabularyTree.column('#1', stretch=NO, minwidth=347, width=200)
    vocabularyTree.column('#2', stretch=NO, minwidth=347, width=200)
    vocabularyTree.column('#3', stretch=NO, minwidth=347, width=200)
    vocabularyTree.column('#4', stretch=NO, minwidth=347, width=400)

    space4 = Label(root, text='\n')
    searchFrame = Frame(root, bg='grey', bd=5)
    searchLabel = Label(searchFrame, text=' Запрос: ', width=14, height=2, bg='grey', fg='white')
    searchEntry = Entry(searchFrame, width=23)
    space41 = Label(searchFrame, text='      ', bg='grey')
    searchButton = Button(searchFrame, text='Найти', width=8, height=2, bg='grey')
    clearSearchButton = Button(searchFrame, text='Помощь', width=8, height=2, bg='grey')

    addMorpologicInfButton = Button(searchFrame, text='Добавить доп. морфологическую информацию', width=40, height=2,
                                    bg='grey')
    clearVocabularyButton = Button(searchFrame, text='Очистить словарь', width=30, height=2, bg='grey')
    deleteElementButton = Button(searchFrame, text='Удалить ', width=30, height=2, bg='grey')

    # Todo: команды для работы с кнопками
    createVocabularyButton_textFile_rtf.config(command=push_table_from_rtf_file)
    createVocabularyButton_textFile_txt.config(command=push_table_from_txt_file)
    createVocabularyButton_textField.config(command=create_vocabulary_from_text_field)
    clearVocabularyButton.config(command=clear_vocabulary)
    deleteElementButton.config(command=delete_item)
    addMorpologicInfButton.config(command=changeInf)
    # searchButton.config(command=get_search_result)
    # clearSearchButton.config(command=show_help_request)
    # clearSearchButton.config(command=show_help_request)

    space0.pack()
    inputFrame.pack()
    inputText.pack()

    space01.pack()
    mainMenuFrame.pack()
    createVocabularyButton_textFile_txt.pack(side='left')
    createVocabularyButton_textFile_rtf.pack(side='left')
    createVocabularyButton_textField.pack(side='left')

    space1.pack()
    vocabularyFrame.pack()
    vocabularyTree.pack()

    space4.pack()
    searchFrame.pack()
    addMorpologicInfButton.pack(side='left')
    clearVocabularyButton.pack(side='left')
    deleteElementButton.pack(side='left')

    popupWindow = Toplevel(root)
    popupWindow.withdraw()
    popupInputText = Entry(popupWindow, width=20)

    root.mainloop()
