import os
import random
import sys
from pathlib import Path
from textwrap import wrap

from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout
import requests
from random import choice

from django.utils.lorem_ipsum import words


class TestPage(QWidget):
    def __init__(self, collection_id, stack, parent):
        super().__init__()
        self.stack = stack
        self.parent = parent
        self.initUI(collection_id)
        self.test_load()
        self.next_word()

    def initUI(self, collection_id):
        self.collection_id = collection_id
        self.layout = QVBoxLayout(self)

        self.status_label = QLabel('Status will be displayed here')
        self.status_label.setObjectName('status_label')
        self.status_label.setMaximumHeight(33)
        self.layout.addWidget(self.status_label)

        self.words_layout = QHBoxLayout()
        self.layout.addLayout(self.words_layout)

        self.cycle_label = QLabel('Cycle 1')
        self.cycle_label.setObjectName('cycle_label')
        self.cycle_label.setMaximumHeight(33)
        self.layout.addWidget(self.cycle_label)

        self.word_button = QPushButton('Word')
        self.word_button.setMinimumHeight(150)
        self.word_button.setObjectName('word_button')
        self.word_button.clicked.connect(self.show_other_word)
        self.layout.addWidget(self.word_button)

        self.button_layout = QHBoxLayout()
        self.layout.addLayout(self.button_layout)

        back_button = QPushButton("Back to main page")
        back_button.setMinimumHeight(70)
        back_button.clicked.connect(self.back_to_main)
        self.layout.addWidget(back_button)

        self.setLayout(self.layout)

        if getattr(sys, 'frozen', False):
            static_css_path = os.path.join(Path(__file__).resolve().parent.parent.parent, "css_pages","test_page_css.css")
        else:
            static_css_path = os.path.join(Path(__file__).resolve().parent.parent.parent, "static", "css_pages", "test_page_css.css")

        with open(static_css_path, "r", encoding='utf-8') as file:
            self.setStyleSheet(file.read())

    def test_load(self):
        try:
            response = requests.get(f'http://127.0.0.1:8000/myapp/show_cards/{self.collection_id}')

            if response.status_code == 200:
                self.words = [x for x in response.json()]
                random.shuffle(self.words)
                self.total_words = len(self.words)
                self.remain_total_words = len(self.words) + 1
                self.word_index = -1
                self.new_cycle = list()
                self.cycle = 1

                display_total_words = QLabel(f"Total words: {self.total_words}")
                display_total_words.setObjectName('display_words')
                self.display_remain_words = QLabel(f"Remaining words: {self.remain_total_words}")
                self.display_remain_words.setObjectName('display_words')
                self.words_layout.addWidget(display_total_words)
                self.words_layout.addWidget(self.display_remain_words)

                button1 = QPushButton('Skip', self)
                button1.clicked.connect(self.next_word)
                button2 = QPushButton('Keep', self)
                button2.clicked.connect(self.keep_word)
                button2.clicked.connect(self.next_word)
                button1.setMinimumHeight(220)
                button2.setMinimumHeight(220)
                self.button_layout.addWidget(button1)
                self.button_layout.addWidget(button2)

            else:
                self.status_label.setText(f"Error loading cards: {response.status_code}")
                print(response.status_code)
        except requests.exceptions.RequestException as e:
            print(e)
            self.status_label.setText(f"Error loading cards: {str(e)}")


    def next_word(self):
        self.word_index += 1
        if self.word_index  < self.total_words:
            self.text_russian = self.words[self.word_index]['text_russian']
            self.text_english = self.words[self.word_index]['text_english']
            self.chosen_word = choice([self.text_russian, self.text_english])
            self.other_word = self.text_russian if self.chosen_word == self.text_english else self.text_english


            self.word_button.setText("\n".join(wrap(self.chosen_word, 30)))
        else:
            if len(self.new_cycle) == 0:
                self.back_to_main()
                return
            self.word_index = -1
            self.words = self.new_cycle
            self.total_words = len(self.new_cycle)
            self.new_cycle = list()
            self.next_word()
            self.remain_total_words += 1
            self.cycle += 1
            self.cycle_label.setText(f"Cycle {self.cycle}")

        self.remain_total_words -= 1
        self.display_remain_words.setText(f"Remaining words: {self.remain_total_words}")

    def keep_word(self):
        new_pair = {'text_russian' : self.text_russian,'text_english': self.text_english}
        self.remain_total_words += 1
        self.new_cycle.append(new_pair)

    def show_other_word(self):
        if self.word_button.text() == "\n".join(wrap(self.chosen_word, 30)):
            self.word_button.setText("\n".join(wrap(self.other_word, 30)))
        else:
            self.word_button.setText("\n".join(wrap(self.chosen_word, 30)))

    def back_to_main(self):
        self.stack.removeWidget(self)
        self.deleteLater()
        self.stack.setCurrentIndex(1)
