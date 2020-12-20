import time
from datetime import datetime

from flask import Flask, request, abort

app = Flask(__name__)
db = [
    {
        'name': 'Вика',
        'text': 'Привет!',
        'time': time.time()
    }, {
        'name': 'Катя',
        'text': 'Привет, Вика',
        'time': time.time()
    }
]


@app.route("/")
def hello():
    return "Привет, это VVL-Chat!"


@app.route("/status")
def status():
    dt = datetime.now()
    return {
        'status': True,
        'name': 'VVL-Chat',
        'time': time.time(),
        'time_v': dt.strftime('%Y/%m/%d %H:%M'),
    }


@app.route("/send", methods=['POST'])
def send_message():
    if not isinstance(request.json, dict):
        return abort(400)

    name = request.json.get('name')
    text = request.json.get('text')

    if not (isinstance(name, str)
            and isinstance(text, str)
            and name
            and text):
        return abort(400)

    new_message = {
        'name': name,
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


app.run()
