from datetime import datetime

import requests
import sys, os, PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
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
        self.timer.start(3000)

    def get_messages(self):
        self.textBrowser.clear()
        self.textBrowser_2.clear()
        self.print_contact(self.lineEdit.text())

        try:
            response = requests.get(self.url + '/messages')
        except:
            return

        response_data = response.json()  # {'messages': messages}

        for message in response_data['messages']:
            self.print_message(self.lineEdit.text(), self.lineEdit_2.text(), message)


    def print_message(self, sender, receiver, message):
        a_list = [sender, receiver]
        b_list = [message['sender'], message['receiver']]
        if sorted(a_list) == sorted(b_list):
            beauty_time = datetime.fromtimestamp(message['time'])
            beauty_time = beauty_time.strftime('%Y/%m/%d %H:%M')
            self.textBrowser.append(beauty_time + ' ' + message['sender'])
            self.textBrowser.append(message['text'])
            self.textBrowser.append('')


    def print_contact(self, sender):
        try:
            response = requests.get(self.url + '/messages')
        except:
            return

        response_data = response.json()  # {'messages': messages}

        contact_list = []
        for message in response_data['messages']:
            if message['sender'] == sender:
                a = message['receiver']
                contact_list.append(a)
        c_set = set(contact_list)
        a = list(sorted(c_set))
        b = len(c_set)
        for i in range(b):
            self.textBrowser_2.append(a[i])
        self.textBrowser_2.append('')


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