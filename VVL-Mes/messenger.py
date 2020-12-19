from datetime import datetime

import requests
import os, PyQt5
from PyQt5 import QtCore, QtWidgets
import ui_imagedialog


pyqt = os.path.dirname(PyQt5.__file__)
os.environ['QT_PLUGIN_PATH'] = os.path.join(pyqt, "Qt/plugins")


class WorkApp(QtWidgets.QMainWindow, ui_imagedialog.Ui_MainWindow):
    def __init__(self, url='http://127.0.0.1:5000'):
        super().__init__()
        self.setupUi(self)

        self.url = url

        self.pushButton.pressed.connect(self.send_message)

        self.after = 0
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.get_messages)
        self.timer.start(1000)

    def get_messages(self):
        try:
            response = requests.get(self.url + '/messages',
                                    params={'after': self.after})
        except:
            return

        response_data = response.json()  # {'messages': messages}

        for message in response_data['messages']:
            self.print_contact(message['sender'])
            self.print_message(message)
            self.after = message['time']


    def print_message(self, sender, receiver, message):
        if message['sender'] == sender and message['receiver'] == receiver or message['sender'] == receiver and message['receiver'] == sender:
            beauty_time = datetime.fromtimestamp(message['time'])
            beauty_time = beauty_time.strftime('%Y/%m/%d %H:%M')
            self.textBrowser.append(beauty_time + ' ' + message['name'])
            self.textBrowser.append(message['text'])
            self.textBrowser.append('')


    def print_contact(self, sender, message):
        try:
            response = requests.get(self.url + '/messages',
                                    params={'after': self.after})
        except:
            return

        response_data = response.json()  # {'messages': messages}

        for message in response_data['messages']:
            contact_list = set()
            if message['sender'] == sender:
                a = message['receiver']
                contact_list.add(a)
            self.listView.append('\n'.join(contact_list))
            self.listView.append('')


    def send_message(self):
        sender = self.lineEdit.text()
        receiver = self.lineEdit_2.text()
        text = self.textEdit.toPlainText()

        try:
            response = requests.post(self.url + '/send', json={
                'sender': sender,
                'receiver': receiver,
                'text': text
            })
        except:
            self.textBrowser.append('Сервер временно недоступен')
            self.textBrowser.append('')
            return

        if response.status_code != 200:
            self.textBrowser.append('Имя или текст не заполнены')
            self.textBrowser.append('')
            return

        self.textEdit.clear()


app = QtWidgets.QApplication([])
window = WorkApp()
window.show()
app.exec_()
