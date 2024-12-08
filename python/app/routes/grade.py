from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..models import Grade, Student, Course, db

grade_bp = Blueprint('grade', __name__)


@grade_bp.route('/grades/', methods=['GET'])
def grades_list():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    grades_paginate = Grade.query.paginate(page=page, per_page=per_page, error_out=False)
    return render_template('grades_list.html', grades=grades_paginate.items, pagination=grades_paginate)


@grade_bp.route('/grades/add', methods=['GET', 'POST'])
def add_grade():
    students = Student.query.all()
    courses = Course.query.all()

    if request.method == 'POST':
        student_id = request.form['student_id']
        course_id = request.form['course_id']
        grade_value = request.form['grade']
        date_graded = request.form['date_graded']

        new_grade = Grade(student_id=student_id, course_id=course_id, grade=grade_value, date_graded=date_graded)

        try:
            db.session.add(new_grade)
            db.session.commit()
            flash("成绩添加成功！", "success")
            return redirect(url_for('grade.grades_list'))
        except Exception as e:
            db.session.rollback()
            flash(f"添加成绩失败，错误信息：{e}", "danger")
            return redirect(url_for('grade.add_grade'))

    return render_template('add_grade.html', students=students, courses=courses)


@grade_bp.route('/grades/edit/<int:grade_id>', methods=['GET', 'POST'])
def edit_grade(grade_id):
    grade = Grade.query.get_or_404(grade_id)
    students = Student.query.all()
    courses = Course.query.all()

    if request.method == 'POST':
        grade.student_id = request.form['student_id']
        grade.course_id = request.form['course_id']
        grade.grade = request.form['grade']
        grade.date_graded = request.form['date_graded']

        try:
            db.session.commit()
            flash("成绩更新成功！", "success")
            return redirect(url_for('grade.grades_list'))
        except Exception as e:
            db.session.rollback()
            flash(f"更新成绩失败，错误信息：{e}", "danger")
            return redirect(url_for('grade.edit_grade', grade_id=grade.id))

    return render_template('edit_grade.html', grade=grade, students=students, courses=courses)


@grade_bp.route('/grades/delete/<int:grade_id>', methods=['GET'])
def delete_grade(grade_id):
    grade = Grade.query.get_or_404(grade_id)
    try:
        db.session.delete(grade)
        db.session.commit()
        flash("成绩删除成功！", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"删除成绩失败，错误信息：{e}", "danger")
    return redirect(url_for('grade.grades_list'))
