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

class Teacher(db.Model):
    __tablename__ = 'teachers'
    teacher_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    contact_no = db.Column(db.String(15))
    email = db.Column(db.String(100), unique=True, nullable=False)
    academy = db.Column(db.String(100), nullable=False)

class Course(db.Model):
    __tablename__ = 'courses'
    course_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    credits = db.Column(db.Integer, nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.teacher_id'))  # 外键
    teacher = db.relationship('Teacher', backref=db.backref('courses', lazy=True))

class Grade(db.Model):
    __tablename__ = 'grades'
    grade_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.course_id'), nullable=False)
    grade = db.Column(db.Float, nullable=False)
    date_graded = db.Column(db.Date, nullable=False)

    # 创建与学生和课程的关系
    student = db.relationship('Student', backref=db.backref('grades', lazy=True))
    course = db.relationship('Course', backref=db.backref('grades', lazy=True))



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

#添加学生
@app.route('/students/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        # 获取表单数据
        name = request.form.get('name')
        gender = request.form.get('gender')
        email = request.form.get('email')
        academy = request.form.get('academy')
        major = request.form.get('major')

        # 验证字段
        if not name or not gender or not email or not academy or not major:
            flash("所有字段均为必填项", "danger")
            return redirect(url_for('add_student'))

        # 创建新学生实例
        new_student = Student(
            name=name,
            gender=gender,
            email=email,
            academy=academy,
            major=major,
            enrollment_date=datetime.utcnow()  # 可以自动设置
        )

        try:
            db.session.add(new_student)
            db.session.commit()
            flash("学生信息添加成功！", "success")
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"添加学生失败: {e}")
            flash("学生信息添加失败，请稍后再试", "danger")

        return redirect(url_for('students_list'))  # 添加成功后返回学生列表页面

    return render_template('add_student.html')  # 显示添加学生页面

#学生信息
@app.route('/students/', methods=['GET'])
def students_list():
    # 获取分页参数
    page = request.args.get('page', 1, type=int)
    per_page = 10
    students_paginate = Student.query.paginate(page=page, per_page=per_page, error_out=False)

    # 渲染 students_info.html 页面并传递数据
    return render_template('students_info.html', students=students_paginate.items, pagination=students_paginate)



# 删除学生
@app.route('/students/delete/<int:student_id>', methods=['GET'])
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)

    try:
        # 先删除相关成绩记录
        grades = Grade.query.filter_by(student_id=student_id).all()
        for grade in grades:
            db.session.delete(grade)

        # 删除学生记录
        db.session.delete(student)
        db.session.commit()
        flash("学生信息删除成功！", "success")
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"删除学生失败: {e}")
        flash("删除学生失败，请稍后再试", "danger")

    return redirect(url_for('students_list'))


# 修改学生
@app.route('/students/edit/<int:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    student = Student.query.get_or_404(student_id)

    if request.method == 'POST':
        name = request.form.get('name')
        gender = request.form.get('gender')
        email = request.form.get('email')
        academy = request.form.get('academy')
        major = request.form.get('major')

        if not name or not gender or not email or not academy or not major:
            flash("所有字段均为必填项", "danger")
            return redirect(url_for('edit_student', student_id=student.id))

        student.name = name
        student.gender = gender
        student.email = email
        student.academy = academy
        student.major = major

        try:
            db.session.commit()
            flash("学生信息修改成功！", "success")
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"修改学生失败: {e}")
            flash("学生信息修改失败，请稍后再试", "danger")

        return redirect(url_for('students_list'))  # 修改后返回学生列表页面

    return render_template('edit_student.html', student=student)


# 查询学生
@app.route('/students/search', methods=['GET'])
def search_students():
    search_query = request.args.get('query', '').strip()
    if not search_query:
        flash("请输入搜索内容", "warning")
        return redirect(url_for('students_list'))

    # 如果是数字，按学生ID查找；如果是字符串，按学生姓名查找
    if search_query.isdigit():
        students = Student.query.filter(Student.student_id == int(search_query)).all()
    else:
        students = Student.query.filter(Student.name.contains(search_query)).all()

    # 添加分页功能
    page = request.args.get('page', 1, type=int)
    per_page = 10
    students_paginate = Student.query.filter(Student.name.contains(search_query)).paginate(page=page, per_page=per_page, error_out=False)

    return render_template('students_info.html', students=students_paginate.items, pagination=students_paginate)

@app.route('/teachers/', methods=['GET'])
def teachers_list():
    # 获取分页参数
    page = request.args.get('page', 1, type=int)
    per_page = 10
    teachers_paginate = Teacher.query.paginate(page=page, per_page=per_page, error_out=False)

    # 渲染教师信息页面并传递数据
    return render_template('teachers_info.html', teachers=teachers_paginate.items, pagination=teachers_paginate)

@app.route('/courses/', methods=['GET'])
def courses_list():
    # 获取分页参数
    page = request.args.get('page', 1, type=int)
    per_page = 10
    courses_paginate = Course.query.paginate(page=page, per_page=per_page, error_out=False)

    # 渲染课程信息页面并传递数据
    return render_template('courses_info.html', courses=courses_paginate.items, pagination=courses_paginate)

@app.route('/teachers/add', methods=['GET', 'POST'])
def add_teacher():
    if request.method == 'POST':
        # 获取表单数据
        name = request.form.get('name')
        gender = request.form.get('gender')
        email = request.form.get('email')
        academy = request.form.get('academy')

        # 验证字段
        if not name or not gender or not email or not academy:
            flash("所有字段均为必填项", "danger")
            return redirect(url_for('add_teacher'))

        # 创建新教师实例
        new_teacher = Teacher(
            name=name,
            gender=gender,
            email=email,
            academy=academy
        )

        try:
            db.session.add(new_teacher)
            db.session.commit()
            flash("教师信息添加成功！", "success")
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"添加教师失败: {e}")
            flash("教师信息添加失败，请稍后再试", "danger")

        return redirect(url_for('teachers_list'))  # 添加成功后返回教师列表页面

    return render_template('add_teacher.html')  # 显示添加教师页面

@app.route('/teachers/delete/<int:teacher_id>', methods=['GET'])
def delete_teacher(teacher_id):
    teacher = Teacher.query.get_or_404(teacher_id)

    try:
        # 删除教师相关课程（如果有）
        courses = Course.query.filter_by(teacher_id=teacher_id).all()
        for course in courses:
            db.session.delete(course)

        # 删除教师记录
        db.session.delete(teacher)
        db.session.commit()
        flash("教师信息删除成功！", "success")
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"删除教师失败: {e}")
        flash("删除教师失败，请稍后再试", "danger")

    return redirect(url_for('teachers_list'))

@app.route('/teachers/edit/<int:teacher_id>', methods=['GET', 'POST'])
def edit_teacher(teacher_id):
    teacher = Teacher.query.get_or_404(teacher_id)

    if request.method == 'POST':
        name = request.form.get('name')
        gender = request.form.get('gender')
        email = request.form.get('email')
        academy = request.form.get('academy')

        if not name or not gender or not email or not academy:
            flash("所有字段均为必填项", "danger")
            return redirect(url_for('edit_teacher', teacher_id=teacher.id))

        teacher.name = name
        teacher.gender = gender
        teacher.email = email
        teacher.academy = academy

        try:
            db.session.commit()
            flash("教师信息修改成功！", "success")
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"修改教师失败: {e}")
            flash("教师信息修改失败，请稍后再试", "danger")

        return redirect(url_for('teachers_list'))  # 修改后返回教师列表页面

    return render_template('edit_teacher.html', teacher=teacher)

@app.route('/teachers/search', methods=['GET'])
def search_teachers():
    search_query = request.args.get('query', '').strip()
    if not search_query:
        flash("请输入搜索内容", "warning")
        return redirect(url_for('teachers_list'))

    # 如果是数字，按教师ID查找；如果是字符串，按教师姓名查找
    if search_query.isdigit():
        teachers = Teacher.query.filter(Teacher.teacher_id == int(search_query)).all()
    else:
        teachers = Teacher.query.filter(Teacher.name.contains(search_query)).all()

    # 添加分页功能
    page = request.args.get('page', 1, type=int)
    per_page = 10
    teachers_paginate = Teacher.query.filter(Teacher.name.contains(search_query)).paginate(page=page, per_page=per_page, error_out=False)

    return render_template('teachers_info.html', teachers=teachers_paginate.items, pagination=teachers_paginate)

@app.route('/courses/add', methods=['GET', 'POST'])
def add_course():
    if request.method == 'POST':
        # 获取表单数据
        course_name = request.form.get('course_name')
        description = request.form.get('description')
        credits = request.form.get('credits')
        teacher_id = request.form.get('teacher_id')

        # 验证字段
        if not course_name or not credits or not teacher_id:
            flash("所有字段均为必填项", "danger")
            return redirect(url_for('add_course'))

        # 创建新课程实例
        new_course = Course(
            course_name=course_name,
            description=description,
            credits=credits,
            teacher_id=teacher_id
        )

        try:
            db.session.add(new_course)
            db.session.commit()
            flash("课程信息添加成功！", "success")
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"添加课程失败: {e}")
            flash("课程信息添加失败，请稍后再试", "danger")

        return redirect(url_for('courses_list'))  # 添加成功后返回课程列表页面

    return render_template('add_course.html')  # 显示添加课程页面

@app.route('/courses/delete/<int:course_id>', methods=['GET'])
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)

    try:
        db.session.delete(course)
        db.session.commit()
        flash("课程信息删除成功！", "success")
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"删除课程失败: {e}")
        flash("删除课程失败，请稍后再试", "danger")

    return redirect(url_for('courses_list'))

@app.route('/courses/edit/<int:course_id>', methods=['GET', 'POST'])
def edit_course(course_id):
    course = Course.query.get_or_404(course_id)

    if request.method == 'POST':
        course_name = request.form.get('course_name')
        description = request.form.get('description')
        credits = request.form.get('credits')
        teacher_id = request.form.get('teacher_id')

        if not course_name or not credits or not teacher_id:
            flash("所有字段均为必填项", "danger")
            return redirect(url_for('edit_course', course_id=course.id))

        course.course_name = course_name
        course.description = description
        course.credits = credits
        course.teacher_id = teacher_id

        try:
            db.session.commit()
            flash("课程信息修改成功！", "success")
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"修改课程失败: {e}")
            flash("课程信息修改失败，请稍后再试", "danger")

        return redirect(url_for('courses_list'))  # 修改后返回课程列表页面

    return render_template('edit_course.html', course=course)

@app.route('/courses/search', methods=['GET'])
def search_courses():
    search_query = request.args.get('query', '').strip()
    if not search_query:
        flash("请输入搜索内容", "warning")
        return redirect(url_for('courses_list'))

    # 如果是数字，按课程ID查找；如果是字符串，按课程名称查找
    if search_query.isdigit():
        courses = Course.query.filter(Course.course_id == int(search_query)).all()
    else:
        courses = Course.query.filter(Course.course_name.contains(search_query)).all()

    # 添加分页功能
    page = request.args.get('page', 1, type=int)
    per_page = 10
    courses_paginate = Course.query.filter(Course.course_name.contains(search_query)).paginate(page=page, per_page=per_page, error_out=False)

    return render_template('courses_info.html', courses=courses_paginate.items, pagination=courses_paginate)




if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
