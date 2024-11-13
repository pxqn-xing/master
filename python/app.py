from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'  # SQLite数据库
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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
        return redirect(url_for('index'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            return redirect(url_for('students', page=1))  # 登录成功，跳转到学生管理页面
        return "用户名或密码错误"
    return render_template('login.html')  # 处理 GET 请求，显示登录页面



@app.route('/students/', defaults={'page': 1})
@app.route('/students/<int:page>')
def students(page):
    per_page = 5
    students = Student.query.paginate(page, per_page, False)
    return render_template('students_info.html', students=students.items, pagination=students)


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
    app.run(debug=True, host='127.0.0.1', port=5000)

