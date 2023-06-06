import datetime
import traceback
import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, static_folder='static')


@app.errorhandler(500)
def handle_500_error(exception):
    trace = traceback.format_exc()
    return f"Error: {trace}", 500


# Define the path to the accounts file
accounts_file = os.path.join(os.path.dirname(__file__), 'accounts.txt')

# Define the path to the posts file
posts_file = os.path.join(os.path.dirname(__file__), 'posts.txt')

# Load existing accounts from the accounts file
accounts = {}
if os.path.exists(accounts_file):
    with open(accounts_file, 'r') as f:
        for line in f:
            username, password = line.strip().split(':')
            accounts[username] = password

# Load existing posts from the posts file
posts = []
if os.path.exists(posts_file):
    with open(posts_file, 'r') as f:
        for line in f:
            try:
                title, author, content, time = line.strip().split(':')
                posts.append({
                    'title': title,
                    'author': author,
                    'content': content,
                    'time': time
                })
            except ValueError:
                # Skip invalid lines in the file
                continue

@app.route('/')
def index():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if username in accounts and accounts[username] == password:
        return redirect(url_for('forum'))
    else:
        return render_template('login.html', error='Invalid username or password')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in accounts:
            return render_template('register.html', error='Username already exists')
        else:
            accounts[username] = password
            with open(accounts_file, 'a') as f:
                f.write(f'{username}:{password}\n')
            return redirect(url_for('index'))
    else:
        return render_template('register.html')


@app.route('/forum')
def forum():
    return render_template('forum.html', posts=posts)


@app.route('/post', methods=['GET', 'POST'])
def post():
    if request.method == 'POST':
        # Handle post request
        username = request.form['username']
        title = request.form['title']
        content = request.form['content']
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        posts.append({
            'title': title,
            'author': username,
            'content': content,
            'time': time
        })
        with open(posts_file, 'a') as f:
            f.write(f'{title}:{username}:{content}:{time}\n')
        return redirect(url_for('forum'))
    else:
        return render_template('post.html')


if __name__ == '__main__':
    app.run()
