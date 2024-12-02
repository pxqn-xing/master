

from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..models import Course, Teacher, db

course_bp = Blueprint('course', __name__)

@course_bp.route('/courses/', methods=['GET'])
def courses_list():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    courses_paginate = Course.query.paginate(page=page, per_page=per_page, error_out=False)
    return render_template('courses_info.html', courses=courses_paginate.items, pagination=courses_paginate)

@course_bp.route('/courses/add', methods=['GET', 'POST'])
def add_course():
    teachers = Teacher.query.all()

    if request.method == 'POST':
        course_name = request.form['course_name']
        description = request.form['description']
        credits = request.form['credits']
        teacher_id = request.form['teacher_id']

        new_course = Course(course_name=course_name, description=description, credits=credits, teacher_id=teacher_id)

        try:
            db.session.add(new_course)
            db.session.commit()
            flash("课程添加成功！", "success")
            return redirect(url_for('course.courses_list'))
        except Exception as e:
            db.session.rollback()
            flash(f"添加课程失败，错误信息：{e}", "danger")
            return redirect(url_for('course.add_course'))

    return render_template('add_course.html', teachers=teachers)

@course_bp.route('/courses/edit/<int:course_id>', methods=['GET', 'POST'])
def edit_course(course_id):
    course = Course.query.get_or_404(course_id)
    teachers = Teacher.query.all()

    if request.method == 'POST':
        course.course_name = request.form['course_name']
        course.description = request.form['description']
        course.credits = request.form['credits']
        course.teacher_id = request.form['teacher_id']

        try:
            db.session.commit()
            flash("课程更新成功！", "success")
            return redirect(url_for('course.courses_list'))
        except Exception as e:
            db.session.rollback()
            flash(f"更新课程失败，错误信息：{e}", "danger")
            return redirect(url_for('course.edit_course', course_id=course.id))

    return render_template('edit_course.html', course=course, teachers=teachers)

@course_bp.route('/courses/delete/<int:course_id>', methods=['GET'])
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    try:
        db.session.delete(course)
        db.session.commit()
        flash("课程删除成功！", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"删除课程失败，错误信息：{e}", "danger")
    return redirect(url_for('course.courses_list'))

@course_bp.route('/course/search',methods=['GET'])
def search_courses():
    search_query = request.args.get('query', '').strip()
    if not search_query:
        flash("请输入搜索内容", "warning")
        return redirect(url_for('course.courses_list'))

    # 如果是数字，按课程ID查找；如果是字符串，按课程名称查找
    if search_query.isdigit():
        courses_paginate = Course.query.filter(Course.course_id == int(search_query))
    else:
        courses_paginate = Course.query.filter(Course.course_name.contains(search_query))

    # 添加分页功能
    page = request.args.get('page', 1, type=int)
    per_page = 10
    courses_paginate = courses_paginate.paginate(page=page, per_page=per_page, error_out=False)

    return render_template('courses_info.html', courses=courses_paginate.items, pagination=courses_paginate)
