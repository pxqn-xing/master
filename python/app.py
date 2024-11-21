from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Flask 应用配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:040712@localhost/students_inf'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.urandom(24)

# 数据库初始化
db = SQLAlchemy(app)

# ------------------- 数据库模型 -------------------
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)  # 明文存储
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Student(db.Model):
    __tablename__ = 'students'
    student_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    contact_no = db.Column(db.String(15), nullable=True)
    email = db.Column(db.String(100), unique=True, nullable=True)
    enrollment_date = db.Column(db.Date, nullable=False)
    academy = db.Column(db.String(100), nullable=False)
    major = db.Column(db.String(100), nullable=False)

# ------------------- 页面路由 -------------------
@app.route('/')
def index():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # 验证表单输入
        if not username or not password or not confirm_password:
            flash("所有字段均为必填项", "danger")
            return redirect(url_for('register'))

        if password != confirm_password:
            flash("密码不匹配，请重新输入", "danger")
            return redirect(url_for('register'))

        # 检查用户名是否已存在
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("用户名已存在，请选择其他用户名", "danger")
            return redirect(url_for('register'))

        # 保存新用户
        new_user = User(username=username, password=password)  # 明文存储

        try:
            db.session.add(new_user)
            db.session.commit()
            flash(f"注册成功！用户名 {username} 已存入数据库。请登录", "success")
            return redirect(url_for('index'))  # 注册成功后跳转到登录页面
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"注册失败: {e}")  # 输出错误日志
            flash(f"注册失败，请稍后再试。错误信息: {e}", "danger")
            return redirect(url_for('register'))

    with app.app_context():
        users = User.query.all()
        print(users)  # 检查是否成功存入用户信息

    return render_template('register.html')

# ------------------- 功能路由 -------------------
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': '未接收到数据'}), 400

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'success': False, 'message': '用户名和密码均为必填项'}), 400

    user = User.query.filter_by(username=username).first()
    if user and user.password == password:  # 明文直接比较
        session['user_id'] = user.id
        session['username'] = user.username
        return jsonify({'success': True, 'message': '登录成功', 'username': user.username}), 200

    return jsonify({'success': False, 'message': '用户名或密码错误'}), 401

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash("您已成功注销", "info")
    return redirect(url_for('index'))

@app.route('/students/', methods=['GET'])
def students_list():
    # 获取分页参数
    page = request.args.get('page', 1, type=int)
    per_page = 10
    students_paginate = Student.query.paginate(page=page, per_page=per_page, error_out=False)

    # 渲染 students_info.html 页面并传递数据
    return render_template('students_info.html', students=students_paginate.items, pagination=students_paginate)

#学生页面
@app.route('/students/', methods=['POST'])
def add_student():
    if request.method == 'POST':
        data = request.form
        name = data.get('name')
        gender = data.get('gender')
        email = data.get('email')
        academy = data.get('academy')
        major = data.get('major')

        new_student = Student(
            name=name,
            gender=gender,
            email=email,
            academy=academy,
            major=major
        )

        db.session.add(new_student)
        db.session.commit()
        return redirect(url_for('students_list'))  # 返回学生列表页面

    return render_template('add_student.html')  # GET 请求时渲染添加学生页面


#删除
@app.route('/students/delete/<int:student_id>', methods=['GET'])
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('students_list'))  # 删除后返回学生列表页面

#修改
@app.route('/students/edit/<int:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    student = Student.query.get_or_404(student_id)

    if request.method == 'POST':
        student.name = request.form.get('name')
        student.gender = request.form.get('gender')
        student.email = request.form.get('email')
        student.academy = request.form.get('academy')
        student.major = request.form.get('major')

        db.session.commit()
        return redirect(url_for('students_list'))  # 修改后返回学生列表页面

    return render_template('edit_student.html', student=student)  # GET 请求时渲染修改页面

#查询
@app.route('/students/search', methods=['GET'])
def search_students():
    search_query = request.args.get('query', '')
    students = Student.query.filter(Student.name.contains(search_query) | Student.student_id.contains(search_query)).all()
    return render_template('students_info.html', students=students)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
