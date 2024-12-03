import time

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit
import requests

from .test_page import TestPage
from PyQt5.QtCore import QThread, pyqtSignal


class LoadCardsThread(QThread):
    cards_loaded = pyqtSignal(list)
    error_occurred = pyqtSignal(str)

    def __init__(self, collection_id):
        super().__init__()
        self.collection_id = collection_id

    def run(self):
        try:
            response = requests.get(f'http://127.0.0.1:8000/myapp/show_cards/{self.collection_id}')
            if response.status_code == 200:
                cards = response.json()
                self.cards_loaded.emit(cards)
            else:
                self.error_occurred.emit(f"Error loading cards: {response.status_code}")
        except requests.exceptions.RequestException as e:
            self.error_occurred.emit(f"Error loading cards: {str(e)}")


class CollectionPage(QWidget):
    def __init__(self, collection_id, collection_name, stack, parent):
        super().__init__()
        self.stack = stack
        self.initUI(collection_name, collection_id)
        # self.load_cards()
        self.parent = parent

        self.load_cards_thread = LoadCardsThread(collection_id)
        self.load_cards_thread.cards_loaded.connect(self.update_cards)
        self.load_cards_thread.error_occurred.connect(self.display_error)
        self.load_cards_thread.start()

    def update_cards(self, cards):
        self.cards_field.clear()
        for card in cards:
            self.cards_field.append(f"{card['text_english']} = {card['text_russian']}")

    def display_error(self, message):
        self.status_label.setText(message)

    def initUI(self, collection_name, collection_id):
        self.collection_id = collection_id
        self.collection_name = collection_name
        layout = QVBoxLayout(self)

        self.status_label = QLabel('Status will be displayed here')
        self.status_label.setObjectName('status_label')
        layout.addWidget(self.status_label)

        self.collection_label = QLabel(f"Collection: {collection_name}")
        self.collection_label.setObjectName('collection_label')
        layout.addWidget(self.collection_label)

        self.cards_field = QTextEdit(self)
        self.cards_field.setPlaceholderText("Enter cards according\nto the template:\nenglish - russian")
        layout.addWidget(self.cards_field)

        start_test_button = QPushButton('Start test', self)
        start_test_button.clicked.connect(self.open_test_page)
        start_test_button.setMinimumHeight(50)
        layout.addWidget(start_test_button)

        add_card_button = QPushButton('Confirm cards', self)
        add_card_button.clicked.connect(self.change_cards)
        add_card_button.setMinimumHeight(50)
        layout.addWidget(add_card_button)

        back_button = QPushButton("Back to main page")
        back_button.clicked.connect(self.back_to_main)
        back_button.setMinimumHeight(50)
        layout.addWidget(back_button)

    # def load_cards(self):
    #     try:
    #         response = requests.get(f'http://127.0.0.1:8000/myapp/show_cards/{self.collection_id}')
    #         if response.status_code == 200:
    #             cards = response.json()
    #             self.cards_field.clear()
    #
    #             for card in cards:
    #                 self.cards_field.append(f"{card['text_english']} = {card['text_russian']}")
    #         else:
    #             print(response.status_code)
    #             self.status_label.setText(f"Error loading cards: {response.status_code}")
    #     except requests.exceptions.RequestException as e:
    #         print(str(e))
    #         self.status_label.setText(f"Error loading cards: {str(e)}")

    def change_cards(self):
        cards_text = self.cards_field.toPlainText().splitlines()
        print(cards_text)
        try:
            if cards_text:
                response = requests.delete(f'http://127.0.0.1:8000/myapp/delete_cards/{self.collection_id}/')

                if response.status_code == 204:
                    for card_text in cards_text:
                        if '=' not in card_text:
                            continue
                        text = card_text.split('=')
                        text_english = text[0].strip(' ')
                        text_russian = text[1].strip(' ')
                        data = {'text_russian': text_russian, 'text_english': text_english}
                        response = requests.post(f'http://127.0.0.1:8000/myapp/add_card/{self.collection_id}/', json=data)

                        if response.status_code == 201:
                            self.status_label.setText('Cards added successfully!')
                        else:
                            self.status_label.setText(f"Error: {response.status_code}")
                else:
                    self.status_label.setText(f"Error deleting cards: {response.status_code}")
            else:
                raise Exception('No cards')
        except Exception as e:
            self.status_label.setText(f"Error confirming cards: {str(e)}")

    def open_test_page(self):
        try:
            self.change_cards()
            test_page = TestPage(self.collection_id, self.stack, self)
            self.stack.addWidget(test_page)
            self.stack.setCurrentWidget(test_page)
        except Exception as e:
            self.status_label.setText(f"{str(e)}")

    def back_to_main(self):
        self.stack.removeWidget(self)
        self.deleteLater()
        self.stack.setCurrentIndex(0)
        self.parent.collection_list.setCurrentRow(self.parent.last_collection)
        self.parent.collection_list.setFocus()
