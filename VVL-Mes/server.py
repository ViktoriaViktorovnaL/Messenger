import time
from datetime import datetime

from flask import Flask, request, abort

app = Flask(__name__)

db = []
c_l = ['Вика', 'Кристина', 'Костя', 'Таня', 'Саша', 'Алиса', 'Денис', 'Максим']


@app.route("/")
def hello():
    return "Привет, это VVL-Messenger!"


@app.route("/status")
def status():
    dt = datetime.now()
    return {
        'status': True,
        'name': 'VVL-Messenger',
        'time': time.time(),
        'time_v': dt.strftime('%Y/%m/%d %H:%M')
    }


@app.route("/send", methods=['POST'])
def send_message():
    if not isinstance(request.json, dict):
        return abort(400)

    sender = request.json.get('sender')
    receiver = request.json.get('receiver')
    text = request.json.get('text')

    if not (isinstance(sender, str)
            and isinstance(receiver, str)
            and isinstance(text, str)
            and sender
            and receiver
            and text):
        return abort(400)

    new_message = {
        'sender': sender,
        'receiver': receiver,
        'text': text,
        'time': time.time()
    }
    db.append(new_message)

    return {'ok': True}


@app.route("/messages")
def get_messages():
    try:
        after = float(request.args.get('after', 0))
    except ValueError:
        return abort(400)

    messages = []
    for message in db:
        if message['time'] > after:
            messages.append(message)

    return {'messages': messages}


@app.route("/contacts")
def get_contacts():
    contacts_list = c_l.copy()

    for message in db:
        contact = message['sender']
        if contact not in c_l:
            contacts_list.append(contact)

    return {'contacts': contacts_list}


app.run()
