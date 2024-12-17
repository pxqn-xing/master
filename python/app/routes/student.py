
from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..models import Student, db
from datetime import datetime
from sqlalchemy.orm import aliased
from sqlalchemy import or_

student_bp = Blueprint('student', __name__)

@student_bp.route('/students/', methods=['GET'])
def students_list():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    students_paginate = Student.query.paginate(page=page, per_page=per_page, error_out=False)
    return render_template('students_info.html', students=students_paginate.items, pagination=students_paginate)

@student_bp.route('/students/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        # 获取表单数据
        name = request.form.get('name')
        gender = request.form.get('gender')
        email = request.form.get('email')
        academy = request.form.get('academy')
        major = request.form.get('major')
        date_of_birth = request.form.get('date_of_birth')  # 获取出生日期

        # 验证字段
        if not name or not gender or not email or not academy or not major or not date_of_birth:
            flash("所有字段均为必填项", "danger")
            return redirect(url_for('student.add_student'))

        # 检查电子邮件是否已存在
        existing_student = Student.query.filter_by(email=email).first()
        if existing_student:
            flash("该电子邮箱已经存在，请使用其他邮箱。", "danger")
            return redirect(url_for('student.add_student'))

        # 创建新学生实例
        try:
            new_student = Student(
                name=name,
                gender=gender,
                email=email,
                academy=academy,
                major=major,
                date_of_birth=datetime.strptime(date_of_birth, '%Y-%m-%d').date(),  # 转换为日期类型
                enrollment_date=datetime.utcnow().date()  # 使用当前日期作为入学日期
            )

            # 添加到数据库
            db.session.add(new_student)
            db.session.commit()

            flash("学生信息添加成功！", "success")
            return redirect(url_for('student.students_list'))  # 添加成功后返回学生列表页面
        except Exception as e:
            db.session.rollback()
            flash("学生信息添加失败，请稍后再试", "danger")
            return redirect(url_for('student.add_student'))  # 添加失败，重定向回添加页面

    return render_template('add_student.html')  # 显示添加学生页面

@student_bp.route('/students/edit/<int:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    student = Student.query.get_or_404(student_id)
    if request.method == 'POST':
        student.name = request.form['name']
        student.gender = request.form['gender']
        student.email = request.form['email']
        student.academy = request.form['academy']
        student.major = request.form['major']

        try:
            db.session.commit()
            flash("学生信息更新成功！", "success")
            return redirect(url_for('student.students_list'))
        except Exception as e:
            db.session.rollback()
            flash(f"更新失败，错误信息：{e}", "danger")
            return redirect(url_for('student.edit_student', student_id=student.id))

    return render_template('edit_student.html', student=student)

@student_bp.route('/students/delete/<int:student_id>', methods=['GET'])
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    try:
        db.session.delete(student)
        db.session.commit()
        flash("学生信息删除成功！", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"删除失败，错误信息：{e}", "danger")

    return redirect(url_for('student.students_list'))

@student_bp.route('/students/search',methods=['GET'])
def search_students():
    search_query = request.args.get('query', '').strip()
    if not search_query:
        flash("请输入搜索内容", "warning")
        return redirect(url_for('student.students_list'))

    # 如果是数字，按学生ID查找；如果是字符串，按学生姓名查找
    if search_query.isdigit():
        students_paginate = Student.query.filter(Student.student_id == int(search_query))
    else:
        students_paginate = Student.query.filter(
            or_(
                Student.name.contains(search_query),  # 按学生姓名查找
                Student.academy.contains(search_query),  # 按学院查找
                Student.major.contains(search_query)  # 按专业查找
            )
        )

    # 添加分页功能
    page = request.args.get('page', 1, type=int)
    per_page = 10
    students_paginate = students_paginate.paginate(page=page, per_page=per_page, error_out=False)

    return render_template('students_info.html', students=students_paginate.items, pagination=students_paginate)