import numpy as _np
import pandas as _pd
import os
import csv
import time
from sklearn.utils import shuffle
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtGui import QFont


class Quiz(QtWidgets.QWidget):
    '''
    Japanese Quiz
    Craig Holliman 2021
    '''

    def __init__(self, reactor):
        super().__init__()

        self._define_directories()

        self._load_vocab(self.alphabet_directory, self.alphabet, self.alphabet_name)
        self._load_vocab(self.missed_directory, self.missed, self.missed_name)
        self._load_vocab(self.vocab_directory, self.vocab, self.vocab_name)
        self._load_vocab(self.all_words_directory, self.all_words, self.all_words_name)

        self.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.reactor = reactor
        self.initUI()

    def _define_directories(self):
        self.alphabet_directory = "alphabets/"
        self.alphabet = []
        self.alphabet_name = []

        self.vocab_directory = "vocab/"
        self.vocab = []
        self.vocab_name = []

        self.missed_directory = "missed/"
        self.missed = []
        self.missed_name = []

        self.all_words_directory = "all-words/"
        self.all_words = []
        self.all_words_name = []

        self.missed_words = "missed/missed-words.csv"
        self.missed_words_reversed = "missed/missed-words-reversed.csv"
        self.missed_letters = "missed/missed-letters.csv"

    def _load_vocab(self, directory, contents, quiz_name):
        for filename in os.listdir(directory):
            if filename.endswith(".csv"):
                name = filename.split('.')[0]
                quiz_name.append(name)
                lesson =  _pd.read_csv(str(directory + filename), skiprows=1, header=None, comment='#')
                contents.append(lesson)
                continue
            else:
                for file in os.listdir(directory + str(filename) + '/'):
                    name = file.split('.')[0]
                    quiz_name.append(name)
                    lesson =  _pd.read_csv(str(directory + str(filename) + '/' + file),
                                           skiprows=1, header=None, comment='#')
                    contents.append(lesson)
                    continue

    def initUI(self):
        font = 'Times'
        character_fontsize = 60
        character_entry_fontsize = 32
        combox_box_fontsize = 16
        characters_remaining_fontsize = 14
        num_of_characters_fontsize = 14
        question_status_fontsize = 18
        percent_correct_fontsize = 14

        self.setWindowIcon(QtGui.QIcon('icon.png'))
        layout = QtWidgets.QGridLayout()
        qBox = QtWidgets.QGroupBox("Select Quiz")
        qBox.setFont(QFont(font, 12))

        subLayout = QtWidgets.QGridLayout()
        qBox.setLayout(subLayout)
        layout.addWidget(qBox, 0, 0)

        QtWidgets.QToolTip.setFont(QFont(font, 18))

        self.select = QtWidgets.QComboBox(self)
        self.select.addItem('all-words-newest-100')
        self.select.addItem('all-words-newest-100-reversed')
        for i in self.all_words_name:
            self.select.addItem(i)
        for i in self.all_words_name:
            temp = i + '-reversed'
            self.select.addItem(temp)
        for i in self.alphabet_name:
            self.select.addItem(i)
        for i in self.missed_name:
            self.select.addItem(i)
        for i in self.vocab_name:
            self.select.addItem(i)
        for i in self.vocab_name:
            temp = i + '-reversed'
            self.select.addItem(temp)
        self.select.setFont(QFont('Times', combox_box_fontsize))
        self.select.activated[str].connect(self.selectActivated)
        subLayout.addWidget(self.select, 0, 0)

        self.character_btn = QtWidgets.QPushButton('', self)
        self.character_btn.setFont(QFont('Times', character_fontsize))
        subLayout.addWidget(self.character_btn, 1, 0, 1, 3)

        self.character_entry = QtWidgets.QLineEdit(self)
        self.character_entry.returnPressed.connect(self.storeValue)
        self.character_entry.setFont(QFont('Times', character_entry_fontsize))
        subLayout.addWidget(self.character_entry, 2, 2, 2, 1)

        # numbers of characters remaining in the given quiz
        self.num_of_characters = QtWidgets.QLabel(self)
        self.num_of_characters.setFont(QFont('Times', num_of_characters_fontsize))
        self.num_of_characters.setText('Characters Remaining: ')
        subLayout.addWidget(self.num_of_characters, 2, 0)

        # question status, correct/incorrect/quiz done
        self.question_status = QtWidgets.QLabel(self)
        self.question_status.setFont(QFont('Times', question_status_fontsize))
        #self.question_status.setWordWrap(True)
        subLayout.addWidget(self.question_status, 0, 2)

        # how you're doing on the quiz
        self.percent_correct = QtWidgets.QLabel(self)
        self.percent_correct.setFont(QFont('Times', percent_correct_fontsize))
        self.percent_correct.setText('Percent Correct: ')
        subLayout.addWidget(self.percent_correct, 3, 0)

        # clear the words currently in the missed quizes
        self.clear_btn = QtWidgets.QPushButton('Clear Missed Words', self)
        self.clear_btn.setFont(QFont('Times', 12))
        self.clear_btn.clicked.connect(self.clear_button)
        subLayout.addWidget(self.clear_btn, 4, 0)

        self.setWindowTitle('日本語のクイズ')

        self.setLayout(layout)
        self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def clear_button(self):
        with open(self.missed_words, 'w') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerow(['english', 'kanji', 'meaning'])
            # placeholder row so that the quiz will load
            writer.writerow(['a', 'b', 'c'])
            writer.writerow(['a', 'b', 'c'])

        with open(self.missed_words_reversed, 'w') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerow(['english', 'kanji', 'meaning'])
            # placeholder row so that the quiz will load
            writer.writerow(['a', 'b', 'c'])
            writer.writerow(['a', 'b', 'c'])

    def selectActivated(self, text):
        self.quiz_text = text
        self.two_column_quiz = False
        self.reversed = False

        if text == 'all-words' or text == 'all-words-reversed':
            if 'reversed' in text.split('-'):
                self.reversed = True
                self.english = _np.array(self.all_words[0][2])
                self.japanese = _np.array(self.all_words[0][1])
                self.meaning = _np.array(self.all_words[0][0])
                self.missed_file = self.missed_words_reversed
            else:
                self.english = _np.array(self.all_words[0][0])
                self.japanese = _np.array(self.all_words[0][1])
                self.meaning = _np.array(self.all_words[0][2])
                self.missed_file = self.missed_words

        if text == 'all-words-newest-100' or text == 'all-words-newest-100-reversed':
            if 'reversed' in text.split('-'):
                self.reversed = True
                self.english = _np.array(self.all_words[0][2][-100:])
                self.japanese = _np.array(self.all_words[0][1][-100:])
                self.meaning = _np.array(self.all_words[0][0][-100:])
                self.missed_file = self.missed_words_reversed
            else:
                self.english = _np.array(self.all_words[0][0][-100:])
                self.japanese = _np.array(self.all_words[0][1][-100:])
                self.meaning = _np.array(self.all_words[0][2][-100:])
                self.missed_file = self.missed_words

        for i in self.alphabet_name:
            if text == i:
                index = self.alphabet_name.index(i)
                self.english = _np.array(self.alphabet[index][0])
                self.japanese = _np.array(self.alphabet[index][1])
                self.two_column_quiz = True
                break

        for i in self.vocab_name:
            if text == i or text == i + '-reversed':
                index = self.vocab_name.index(i)
                if 'reversed' in text.split('-'):
                    self.reversed = True
                    self.english = _np.array(self.vocab[index][2])
                    self.japanese = _np.array(self.vocab[index][1])
                    self.meaning = _np.array(self.vocab[index][0])
                    self.missed_file = self.missed_words_reversed
                else:
                    self.english = _np.array(self.vocab[index][0])
                    self.japanese = _np.array(self.vocab[index][1])
                    self.meaning = _np.array(self.vocab[index][2])
                    self.missed_file = self.missed_words
                break

        for i in self.missed_name:
            if text == i:
                index = self.missed_name.index(i)
                if 'reversed' in text.split('-'):
                    self.reversed = True
                    self.english = _np.array(self.missed[index][2])
                    self.japanese = _np.array(self.missed[index][1])
                    self.meaning = _np.array(self.missed[index][0])
                    self.missed_file = self.missed_words_reversed
                else:
                    self.english = _np.array(self.missed[index][0])
                    self.japanese = _np.array(self.missed[index][1])
                    self.meaning = _np.array(self.missed[index][2])
                    self.missed_file = self.missed_words
                break

        self.button_init()

        if self.two_column_quiz:
            self.english, self.japanese = shuffle(self.english, self.japanese)
        else:
            self.english, self.japanese, self.meaning = shuffle(self.english, self.japanese, self.meaning)

        self.total_number = self.japanese.size
        self.num_of_characters.setText('Characters Remaining: ' + str(self.japanese.size) + '/' + str(self.total_number))
        self.character_btn.setText(self.japanese[1])

    def button_init(self):
        self.character_entry.setText('')
        self.question_status.setText('')
        self.character_entry.setFocus()
        self.num_correct = 0
        self.num_total = 0

    def storeValue(self):
        self.text = self.character_entry.text()

        # if quizzing one of the alphabet quizzes
        if self.two_column_quiz:
            self.two_column_store()

        if not self.two_column_quiz:
            self.three_column_store()

    def two_column_store(self):
        # if there is only one word left in the quiz
        if self.japanese.size == 1:
            # correct answer is given
            if self.text in self.english[0].split() or self.text == self.english[0]:
                self.quiz_is_done()
            # you get the question wrong
            else:
                self.question_status.setText('Incorrect, ' + str(self.japanese[0]) + ': ' + str(self.english[0]))
                self.character_entry.setText('')
        # more than one word left in the quiz
        else:
            self.num_total += 1
            # correct answer is given
            if self.text in self.english[1].split() or self.text == self.english[1]:
                self.num_correct += 1
                self.question_status.setText('Correct, ' + str(self.japanese[1]) + ': ' + str(self.english[1]))
                self.japanese = _np.delete(self.japanese, 1)
                self.english = _np.delete(self.english, 1)
            # you get the question wrong
            else:
                self.question_status.setText('Incorrect, ' + str(self.japanese[1]) + ': ' + str(self.english[1]))
                with open(self.missed_letters, 'a', encoding='utf-8') as csvfile:
                    fieldnames = ['hiragana', 'character']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writerow({'hiragana': str(self.english[1]), 'character': str(self.japanese[1])})

                self.english, self.japanese = shuffle(self.english, self.japanese)
            # check how many are left
            if self.japanese.size == 1:
                self.character_btn.setText(self.japanese[0])
            else:
                self.character_btn.setText(self.japanese[1])
            self.character_entry.setText('')
            self.num_of_characters.setText('Characters Remaining: ' + str(self.japanese.size) + '/' + str(self.total_number))
            self.percent_correct.setText('Percent Correct: ' + str(round(self.num_correct/self.num_total * 100, 2)) + '%')

    def three_column_store(self):
        # if there is only one word left in the quiz
        if self.japanese.size == 1:
            # correct answer is given
            if self.text in self.english[0].split() or self.text == self.english[0]:
                self.quiz_is_done()
            # you get the question wrong
            else:
                self.question_status.setText('Incorrect, ' + str(self.japanese[0]) + ': ' + str(self.english[0]) + ', ' + str(self.meaning[0]))
                self.character_entry.setText('')
        # there is more than one word left in the quiz
        else:
            self.num_total += 1
            # correct answer is given
            if self.text in self.english[1].split() or self.text == self.english[1]:
                self.num_correct += 1
                self.question_status.setText('Correct, ' + str(self.japanese[1]) + ': ' + str(self.meaning[1]) + ' - ' + str(self.english[1]))
                self.japanese = _np.delete(self.japanese, 1)
                self.english = _np.delete(self.english, 1)
                self.meaning = _np.delete(self.meaning, 1)
            # you get the question wrong
            else:
                self.question_status.setText('Incorrect, ' + str(self.japanese[1]) + ': ' + str(self.english[1]) + ', ' + str(self.meaning[1]))
                with open(self.missed_file, 'a', encoding='utf-8') as csvfile:
                    fieldnames = ['english', 'japanese', 'meaning']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    if self.reversed == False:
                        writer.writerow({'english': str(self.english[1]), 'japanese': str(self.japanese[1]), 'meaning': str(self.meaning[1])})
                    else:
                        writer.writerow({'english': str(self.meaning[1]), 'japanese': str(self.japanese[1]), 'meaning': str(self.english[1])})
                self.english, self.japanese, self.meaning = shuffle(self.english, self.japanese, self.meaning)
            # check how many are left
            if self.japanese.size == 1:
                self.character_btn.setText(self.japanese[0])
            else:
                self.character_btn.setText(self.japanese[1])
            self.character_entry.setText('')
            self.num_of_characters.setText('Characters Remaining: ' + str(self.japanese.size) + '/' + str(self.total_number))
            self.percent_correct.setText('Percent Correct: ' + str(round(self.num_correct/self.num_total * 100, 2)) + '%')

    def quiz_is_done(self):
        self.question_status.setText('All done!')
        self.num_of_characters.setText("")
        self.character_btn.setText(':D')
        self.character_entry.setText('')
        self.num_of_characters.setText('Go Again!')

    def closeEvent(self, x):
        self.stop = True
        self.reactor.stop()


if __name__ == '__main__':
    a = QtWidgets.QApplication([])
    import qt5reactor
    qt5reactor.install()
    from twisted.internet import reactor
    client = Quiz(reactor)
    client.show()
    reactor.run()
