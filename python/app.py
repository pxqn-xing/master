from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.urandom(24)
db = SQLAlchemy(app)


# 用户表
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)


# 学生表
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    college = db.Column(db.String(100), nullable=False)
    major = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    parent_contact = db.Column(db.String(20), nullable=False)


# 创建数据库
with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirmPassword']

        if password != confirm_password:
            flash("密码不匹配，请重新输入", "danger")
            return redirect(url_for('register'))

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("用户名已存在，请选择其他用户名", "danger")
            return redirect(url_for('register'))

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash("注册成功！请登录", "success")
        return redirect(url_for('index'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()

        if user:
            session['user_id'] = user.id
            session.permanent = True
            flash("登录成功", "success")
            return redirect(url_for('students', page=1))
        flash("用户名或密码错误", "danger")
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("您已成功注销", "info")
    return redirect(url_for('index'))


@app.route('/students/', defaults={'page': 1})
@app.route('/students/<int:page>')
def students(page):
    if 'user_id' not in session:
        flash("请先登录", "warning")
        return redirect(url_for('index'))

    per_page = 5
    students = Student.query.paginate(page, per_page, error_out=False)

    return jsonify({
        'students': [student.__dict__ for student in students.items],
        'pagination': {
            'current_page': students.page,
            'total_pages': students.pages,
            'has_prev': students.has_prev,
            'has_next': students.has_next,
            'prev_num': students.prev_num,
            'next_num': students.next_num
        }
    })


if __name__ == '__main__':
    app.run(debug=True)
