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

        self.pushButton_2.pressed.connect(self.print_contact)
        self.pushButton.pressed.connect(self.send_message)

        self.after = 0
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.get_messages)
        self.timer.start(6000)


    def get_messages(self):
        self.textBrowser.clear()

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


    def print_contact(self):
        self.textBrowser_2.clear()
        try:
            response_c = requests.get(self.url + '/contacts')
        except:
            return

        response_contact = response_c.json()  # {'contacts': contact_list}

        sender = self.lineEdit.text()

        contact_list = response_contact['contacts']
        c_list = sorted(contact_list)

        if sender not in contact_list:
            self.textBrowser.append('Добро пожаловать в Мессенджер')
        else:
            c_list.remove(sender)
        b = len(c_list)
        for i in range(b):
            self.textBrowser_2.append(c_list[i])


    def send_message(self):
        sender = self.lineEdit.text()
        receiver = self.lineEdit_2.text()
        text = self.textEdit.toPlainText()

        try:
            response_c = requests.get(self.url + '/contacts')
        except:
            return

        response_contact = response_c.json()  # {'contacts': contact_list}

        try:
            if receiver not in response_contact['contacts']:
                self.textBrowser.append('Указанный получатель не является пользователем')
                self.textBrowser.append('')
                raise Exception('Ошибка списка пользователей')
        except:
            self.textBrowser.append('Ошибка списка пользователей')
            self.textBrowser.append('')
            return

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
