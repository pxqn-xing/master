from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 用于会话管理（登录状态等）

# 连接数据库函数
def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',          # 数据库主机
        user='your_username',      # 数据库用户名
        password='your_password',  # 数据库密码
        database='your_database'   # 数据库名称
    )
    return conn

# 首页路由（显示用户列表）
@app.route('/')
def home():
    if 'user_id' in session:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM users')
        users = cursor.fetchall()
        conn.close()
        return render_template('home.html', users=users)
    else:
        return redirect(url_for('login'))

# 登录路由
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # 查询数据库检查用户
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['user_id'] = user['id']  # 登录成功，保存用户 ID 到 session
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password!')
            return redirect(url_for('login'))

    return render_template('login.html')

# 注册路由
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # 检查用户名是否已存在
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash('Username already exists!')
            return redirect(url_for('register'))

        # 插入新用户
        cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, password))
        conn.commit()
        conn.close()

        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))

    return render_template('register.html')

# 退出登录路由
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
