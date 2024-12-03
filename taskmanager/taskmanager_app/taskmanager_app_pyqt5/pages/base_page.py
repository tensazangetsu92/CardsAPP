import sys
from pathlib import Path

import PyQt5
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QHBoxLayout, \
    QListWidget, QListWidgetItem, QStackedWidget, QMessageBox, QInputDialog
from PyQt5.uic.properties import QtCore
from django.conf.urls.static import static

from .collection_page import CollectionPage
import subprocess
import os
import requests


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.static_dir = os.path.join(Path(__file__).resolve().parent.parent.parent, "static")
        self.start_django_server()
        self.initUI()
        self.last_collection = None
        self.load_collections()

    def start_django_server(self):
        django_command = [r"C:\\Users\\alex\\PycharmProjects\\TaskManager\\.venv\\Scripts\\python.exe",
                          r"C:\\Users\\alex\\PycharmProjects\\TaskManager\\taskmanager\\manage.py", "runserver", '--noreload']

        try:
            if os.name == 'nt':
                self.server_process = subprocess.Popen(django_command, creationflags=subprocess.CREATE_NO_WINDOW,
                                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            else:
                self.server_process = subprocess.Popen(django_command, preexec_fn=os.setsid)
        except Exception as e:
            print(f"Ошибка при запуске сервера Django: {str(e)}")


    def initUI(self):
        self.setWindowTitle('CardsAPP')
        self.setFixedSize(550, 700)
        self.confirmation_dialog = None
        self.stack = QStackedWidget(self)
        self.main_page = QWidget()
        layout = QVBoxLayout(self.main_page)
        self.collection_input = QLineEdit(self.main_page)
        self.collection_input.setObjectName('collection_input')
        self.collection_input.setPlaceholderText("Enter collection name")
        self.collection_input.returnPressed.connect(self.add_collection)
        layout.addWidget(self.collection_input)

        add_collection_button = QPushButton('Add Collection', self.main_page)
        add_collection_button.clicked.connect(self.add_collection)
        add_collection_button.setMinimumHeight(70)
        layout.addWidget(add_collection_button)

        self.status_label = QLabel('Status will be displayed here')
        self.status_label.setObjectName('status_label')
        layout.addWidget(self.status_label)

        self.collection_list = QListWidget(self.main_page)
        self.collection_list.itemDoubleClicked.connect(self.open_collection_page)
        layout.addWidget(self.collection_list)

        self.stack.addWidget(self.main_page)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.stack)

        if getattr(sys, 'frozen', False):
            page_css_path = os.path.join(self.static_dir,"css_pages","base_page_css.css")
        else:
            page_css_path = os.path.join(self.static_dir,"css_pages","base_page_css.css")
        with open(page_css_path, "r", encoding='utf-8') as file:
            self.setStyleSheet(file.read())

    def load_collections(self):
        try:
            response = requests.get('http://127.0.0.1:8000/myapp/show_collections/')
            if response.status_code == 200:
                collections = response.json()
                self.collection_list.clear()
                count = 0
                for collection in collections:
                    list_item = QListWidgetItem(self.collection_list)
                    list_item.setData(Qt.UserRole, collection['id'])
                    list_item.setData(Qt.UserRole + 1, collection['collection_name'])
                    list_item.setData(Qt.UserRole + 2, count)

                    item_widget = QWidget()
                    item_widget.setMinimumHeight(60)
                    item_widget.setObjectName("item_widget")
                    layout = QHBoxLayout()

                    collection_label = QLabel(collection['collection_name'])

                    #static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..', '..','static')


                    rename_button = QPushButton('', self)
                    rename_button.setIcon(QIcon(os.path.join(self.static_dir,'images','free-icon-edit-1159633.png')))
                    rename_button.setIconSize(PyQt5.QtCore.QSize(40, 30))
                    rename_button.clicked.connect(lambda _, id=collection['id']: self.rename_collection(id))
                    rename_button.setMinimumHeight(60)
                    # free-icon-delete-1345823.png
                    # free-icon-delete-1214428.png
                    # free-icon-delete-2907762.png
                    # free-icon-delete-3395538.png

                    delete_button = QPushButton('', self)
                    delete_button.setIcon(QIcon(os.path.join(self.static_dir, 'images', 'free-icon-delete-1345823.png')))
                    delete_button.setIconSize(PyQt5.QtCore.QSize(40, 30))
                    delete_button.clicked.connect(lambda _, id=collection['id']: self.delete_collection(id))
                    delete_button.setMinimumHeight(60)

                    layout.addWidget(collection_label)
                    layout.addStretch()
                    layout.addWidget(rename_button)
                    layout.addWidget(delete_button)
                    item_widget.setLayout(layout)

                    list_item.setSizeHint(item_widget.sizeHint())
                    self.collection_list.setItemWidget(list_item, item_widget)
                    count += 1

                if self.collection_list.count() > 0:
                    self.collection_list.setCurrentRow(self.collection_list.count() - 1)
                    self.collection_list.setFocus()



            else:
                self.status_label.setText(f"Error loading collections: {response.status_code}")
        except requests.exceptions.RequestException as e:
            self.status_label.setText(f"Error loading collections: {str(e)}")

    def add_collection(self):
        collection_name = self.collection_input.text()
        if collection_name:
            data = {'collection_name': collection_name}
            response = requests.post('http://127.0.0.1:8000/myapp/add_collection/', json=data)

            if response.status_code == 201:
                self.status_label.setText('Collection added successfully!')
                self.load_collections()
                self.collection_input.setText('')
                self.collection_list.setCurrentRow(self.collection_list.count() - 1)
                self.collection_list.setFocus()
            else:
                self.status_label.setText(f"Error: {response.status_code}")
        else:
            self.status_label.setText('Please enter a collection name!')

    def rename_collection(self, collection_id):
        collection_name = self.get_collection_name_by_id(collection_id)
        if not collection_name:
            self.status_label.setText('Collection not found!')
            return

        new_name, ok = QInputDialog.getText(self, "Rename Collection", "Enter new collection name:",
                                            text=collection_name)

        if ok and new_name:
            data = {'collection_name': new_name}
            try:
                response = requests.put(f'http://127.0.0.1:8000/myapp/rename_collection/{collection_id}/', json=data)

                if response.status_code == 200:
                    self.status_label.setText('Collection renamed successfully!')
                    self.load_collections()
                else:
                    self.status_label.setText(f"Error renaming collection: {response.status_code}")
            except requests.exceptions.RequestException as e:
                self.status_label.setText(f"Error renaming collection: {str(e)}")
        else:
            self.status_label.setText('Rename operation cancelled.')
    def get_collection_name_by_id(self, collection_id):
        for i in range(self.collection_list.count()):
            item = self.collection_list.item(i)
            if item.data(Qt.UserRole) == collection_id:
                return item.data(Qt.UserRole + 1)
        return None

    def delete_collection(self, collection_id):
        self.confirmation_dialog = QMessageBox(self)
        self.confirmation_dialog.setWindowTitle("Delete Confirmation")
        self.confirmation_dialog.setText("Are you sure you want to delete this collection?")

        no_button = self.confirmation_dialog.addButton("No", QMessageBox.RejectRole)
        yes_button = self.confirmation_dialog.addButton("Yes", QMessageBox.AcceptRole)

        self.confirmation_dialog.exec_()

        if self.confirmation_dialog.clickedButton() == yes_button:
            try:
                if collection_id:
                    response = requests.delete(f'http://127.0.0.1:8000/myapp/delete_collection/{collection_id}/')
                    if response.status_code == 204:
                        self.status_label.setText('Collection deleted successfully!')
                        self.load_collections()
                    else:
                        self.status_label.setText(f"Error: {response.status_code}")
                else:
                    self.status_label.setText('No collection ID provided!')
            except requests.exceptions.RequestException as e:
                self.status_label.setText(f"Error deleting collection: {str(e)}")
        else:
            self.status_label.setText('Collection deletion cancelled.')

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            current_item = self.collection_list.currentItem()
            if current_item:
                self.open_collection_page(current_item)
        elif self.confirmation_dialog and self.confirmation_dialog.isVisible():
            if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
                self.confirmation_dialog.done(QMessageBox.Yes)
                self.confirmation_dialog = None

    def closeEvent(self, event):
        if self.confirmation_dialog:
            self.confirmation_dialog.close()
            self.confirmation_dialog = None
        if self.server_process:
            self.server_process.terminate()
        event.accept()

    def open_collection_page(self, item):
        collection_id = item.data(Qt.UserRole)
        collection_name = item.data(Qt.UserRole + 1)

        collection_page = CollectionPage(collection_id, collection_name, self.stack, self)
        self.last_collection = item.data(Qt.UserRole + 2)
        self.stack.addWidget(collection_page)
        self.stack.setCurrentWidget(collection_page)


if __name__ == "__main__":
    app = QApplication([])
    window = App()
    window.show()
    app.exec_()
