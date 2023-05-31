from flask import Flask, render_template, request
import datetime

app = Flask(__name__)

messages = []


def save_messages():
    with open('messages.txt', 'w', encoding='utf-8') as f:
        for message in messages:
            f.write(message[0] + ',' + message[1] + ',' + message[2] + '\n')


def load_messages():
    with open('messages.txt', 'r', encoding='utf-8') as f:
        for line in f.read().splitlines():
            time, content, user = line.split(',')
            messages.append((time, content, user))


try:
    load_messages()
except FileNotFoundError:
    pass


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user = request.form['user']
        message = request.form['message']
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        messages.append((time, message, user))
        save_messages()

    return render_template('index.html', messages=messages)


if __name__ == '__main__':
    app.run()