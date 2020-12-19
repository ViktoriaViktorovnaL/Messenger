import time
from datetime import datetime

sender = input('Введите имя: ')

receiver = input('Введите имя: ')


message1 = {
    'sender': 'Вика',
    'receiver': 'Катя',
    'text': 'Привет!',
    'time': time.time()
}
message2 = {
    'sender': 'Катя',
    'receiver': 'Вика',
    'text': 'Привет, Вика',
    'time': time.time()
}

message3 = {
    'sender': 'Вика',
    'receiver': 'Катя',
    'text': 'Пошли по магазинам?',
    'time': time.time()
}
message4 = {
    'sender': 'Вика',
    'receiver': 'Оля',
    'text': 'Привет, Оля, пошли по магазинам?',
    'time': time.time()
}


db = [message1, message2, message3, message4]


def send_message(sender, receiver, text):
    new_message = {
        'sender': sender,
        'receiver': receiver,
        'text': text,
        'time': time.time()
     }
    db.append(new_message)


def get_messages(after=0):
    messages = []
    for message in db:
        if message['time'] > after:
                messages.append(message)
    return messages


def print_messages(sender, receiver, messages):
    for message in messages:
        beauty_time = datetime.fromtimestamp(message['time'])
        beauty_time = beauty_time.strftime('%Y/%m/%d %H:%M')
        if message['sender'] == sender and message['receiver'] == receiver or message['sender'] == receiver and message['receiver'] == sender:
            print(beauty_time, message['sender'])
            print(message['text'])
            print()


print_messages(sender, receiver, db)


def print_contact(sender, messages):
    contact_list = set()
    for message in messages:
        if message['sender'] == sender:
            a = message['receiver']
            contact_list.add(a)
    print('\n'.join(contact_list))
    print()


print_contact(sender, db)
