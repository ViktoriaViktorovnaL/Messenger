# Messenger

Сначала создала просто общий чат, проверила работоспособность. Всё ок. Потом перешла к месенджеру.

Устанавливала: flask, requests, PyQt5

Для формирования интерфейса использовала Qt Designer

Скачиваkf с 
https://build-system.fman.io/qt-designer-download

Сделала оболочку месенджера.
Созданный файл ______.ui импортировала в Python:
в терминале (верт.окружение) >>pyuic5 vvl-messenger.ui -o ui_imagedialog.py

Программа выдавала ошибку:
qt.qpa.plugin: Could not find the Qt platform plugin "windows" in ""
This application failed to start because no Qt platform plugin could be initialized. Reinstalling the application may fix this problem.

Добавила к коду (на coderoad нашла):
pyqt = os.path.dirname(PyQt5.__file__)
os.environ['QT_PLUGIN_PATH'] = os.path.join(pyqt, "Qt/plugins")

Чат работал, проверила на своем компе и на ноуте.

Сегодня перешла к работе с мессенджером, дополнила словарь (сообщение) аргументами отправитель и получатель, сделала список контактов, но что-то пошло не так.
