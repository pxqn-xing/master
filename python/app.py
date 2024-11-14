from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'  # SQLite数据库
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.urandom(24)  # 用于 session 加密
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

    # 添加测试数据（如果数据库为空）
    if User.query.count() == 0:
        sample_users = [
            User(username='username', password='password'),  # 默认的测试用户
        ]
        db.session.add_all(sample_users)
        db.session.commit()

    if Student.query.count() == 0:
        sample_students = [
            Student(
                student_id='2021001',
                name='John Doe',
                college='Computer Science',
                major='Software Engineering',
                contact='1234567890',
                address='123 Main St, City, Country',
                parent_contact='0987654321'
            ),
            Student(
                student_id='2021002',
                name='Jane Smith',
                college='Engineering',
                major='Electrical Engineering',
                contact='2345678901',
                address='456 Oak St, City, Country',
                parent_contact='1234509876'
            ),
            Student(
                student_id='2021003',
                name='Sam Johnson',
                college='Science',
                major='Physics',
                contact='3456789012',
                address='789 Pine St, City, Country',
                parent_contact='2345610987'
            ),
            Student(
                student_id='2021004',
                name='Emily Davis',
                college='Mathematics',
                major='Applied Mathematics',
                contact='4567890123',
                address='101 Maple St, City, Country',
                parent_contact='3456721098'
            ),
            Student(
                student_id='2021005',
                name='Michael Brown',
                college='Arts',
                major='English Literature',
                contact='5678901234',
                address='202 Birch St, City, Country',
                parent_contact='4567832109'
            )
        ]
        db.session.add_all(sample_students)
        db.session.commit()


# 路由：主页（登录页面）
@app.route('/')
def index():
    return render_template('login.html')


# 路由：注册页面
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirmPassword']

        if password != confirm_password:
            return "密码不匹配"

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('index'))  # 注册成功，跳转到登录页面
    return render_template('register.html')


# 路由：登录页面
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            session['user_id'] = user.id  # 保存用户登录状态
            return redirect(url_for('students', page=1))  # 登录成功，跳转到学生管理页面
        return "用户名或密码错误"
    return render_template('login.html')  # 处理 GET 请求，显示登录页面


# 路由：学生信息管理页面
@app.route('/students/', defaults={'page': 1})
@app.route('/students/<int:page>')
def students(page):
    if 'user_id' not in session:
        return redirect(url_for('index'))  # 如果未登录，跳转回登录页面

    per_page = 5
    students = Student.query.paginate(page, per_page, error_out=False)

    # 返回分页后的学生数据
    return jsonify({
        'students': [{
            'id': student.id,
            'studentId': student.student_id,
            'studentName': student.name,
            'college': student.college,
            'major': student.major,
            'contact': student.contact,
            'address': student.address,
            'parentContact': student.parent_contact
        } for student in students.items],
        'pagination': {
            'current_page': students.page,
            'total_pages': students.pages,
            'has_prev': students.has_prev,
            'has_next': students.has_next,
            'prev_num': students.prev_num,
            'next_num': students.next_num
        }
    })


# 路由：添加学生信息
@app.route('/add_student', methods=['POST'])
def add_student():
    data = request.get_json()  # 接收 JSON 格式数据
    student_id = data['studentId']
    name = data['studentName']
    college = data['college']
    major = data['major']
    contact = data['contact']
    address = data['address']
    parent_contact = data['parentContact']

    new_student = Student(
        student_id=student_id,
        name=name,
        college=college,
        major=major,
        contact=contact,
        address=address,
        parent_contact=parent_contact
    )
    db.session.add(new_student)
    db.session.commit()

    return jsonify({'message': '学生信息已添加'}), 201


# 路由：删除学生信息
@app.route('/delete_student/<int:id>', methods=['DELETE'])
def delete_student(id):
    student = Student.query.get(id)
    if student:
        db.session.delete(student)
        db.session.commit()
        return jsonify({'message': '学生信息已删除'}), 200
    return jsonify({'message': '学生未找到'}), 404


if __name__ == '__main__':
    # 获取端口号（默认 5000），可以通过环境变量 PORT 来修改
    port = int(os.environ.get('PORT', 5000))  # 如果没有设置环境变量 PORT，默认使用 5000
    print(f"Starting server on port {port}")

    # 使用 wsgiref 的 make_server 启动 Flask 应用
    from wsgiref.simple_server import make_server

    httpd = make_server('127.0.0.1', port, app)

    # 启动应用
    httpd.serve_forever()
