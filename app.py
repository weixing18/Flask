from flask import Flask, render_template, request, redirect, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key'

users = {}  # 用户信息存储
messages = []  # 留言信息存储

# 读取密码文件
def read_password_file():
    with open('password.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if line:
                username, password = line.split(':')
                users[username] = password

# 注册登录选择页面
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# 注册页面
@app.route('/register', methods=['GET'])
def register_form():
    return render_template('register.html')

# 注册功能
@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    
    if username in users:
        return '该用户名已被注册'
    
    users[username] = password
    
    with open('password.txt', 'a') as f:
        f.write(f'{username}:{password}\n')
    
    return redirect('/')

# 登录页面
@app.route('/login', methods=['GET'])
def login_form():
    return render_template('login.html')

# 登录功能
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    if username not in users:
        return '该用户名不存在'
    
    if users[username] != password:
        return '密码错误'
    
    session['username'] = username
    
    return redirect('/message')

# 留言板页面
@app.route('/message', methods=['GET', 'POST'])
def message():
    if 'username' not in session:
        return redirect('/login')
    
    if request.method == 'POST':
        username = session['username']
        content = request.form['message']
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        messages.append({'username': username, 'content': content, 'timestamp': timestamp})
    
    return render_template('message.html', username=session['username'], messages=messages)

if __name__ == '__main__':
    read_password_file()  # 读取密码文件
    app.run()
