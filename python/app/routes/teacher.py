from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..models import Teacher, db

teacher_bp = Blueprint('teacher', __name__)

@teacher_bp.route('/teachers/', methods=['GET'])
def teachers_list():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    teachers_paginate = Teacher.query.paginate(page=page, per_page=per_page, error_out=False)
    return render_template('teachers_info.html', teachers=teachers_paginate.items, pagination=teachers_paginate)

@teacher_bp.route('/teachers/add', methods=['GET', 'POST'])

@teacher_bp.route('/teachers/add', methods=['GET', 'POST'])
def add_teacher():
    if request.method == 'POST':
        name = request.form['name']
        gender = request.form['gender']
        email = request.form['email']
        academy = request.form['academy']

        # Check if the required fields are filled
        if not name or not gender or not email or not academy:
            flash("所有字段必须填写", "danger")
            return render_template('add_teacher.html')

        # Check if the email already exists
        existing_teacher = Teacher.query.filter_by(email=email).first()
        if existing_teacher:
            flash("该邮箱已被注册", "danger")
            return render_template('add_teacher.html')

        try:
            new_teacher = Teacher(
                name = name,
                gender = gender,
                email = email,
                academy = academy
            )

            db.session.add(new_teacher)
            db.session.commit()
            flash("教师添加成功！", "success")
            return redirect(url_for('teacher.teachers_list'))
        except Exception as e:
            db.session.rollback()
            flash(f"添加教师失败，错误信息：{e}", "danger")
            return redirect(url_for('teacher.add_teacher'))

    return render_template('add_teacher.html')

@teacher_bp.route('/teachers/edit/<int:teacher_id>', methods=['GET', 'POST'])
def edit_teacher(teacher_id):
    teacher = Teacher.query.get_or_404(teacher_id)

    if request.method == 'POST':
        teacher.name = request.form['name']
        teacher.gender = request.form['gender']
        teacher.email = request.form['email']
        teacher.academy = request.form['academy']

        try:
            db.session.commit()
            flash("教师信息更新成功！", "success")
            return redirect(url_for('teacher.teachers_list'))
        except Exception as e:
            db.session.rollback()
            flash(f"更新教师信息失败，错误信息：{e}", "danger")
            return redirect(url_for('teacher.edit_teacher', teacher_id=teacher.teacher.id))

    return render_template('edit_teacher.html', teacher=teacher)

@teacher_bp.route('/teachers/delete/<int:teacher_id>', methods=['GET'])
def delete_teacher(teacher_id):
    teacher = Teacher.query.get_or_404(teacher_id)
    try:
        db.session.delete(teacher)
        db.session.commit()
        flash("教师删除成功！", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"删除教师失败，错误信息：{e}", "danger")
    return redirect(url_for('teacher.teachers_list'))

@teacher_bp.route('/teachers/search', methods=['GET'])
def search_teachers():
    search_query = request.args.get('query', '').strip()
    if not search_query:
        flash("请输入搜索内容", "warning")
        return redirect(url_for('teacher.teachers_list'))

    # 如果是数字，按教师ID查找；如果是字符串，按教师姓名查找
    if search_query.isdigit():
        teachers_paginate = Teacher.query.filter(Teacher.teacher_id == int(search_query))
    else:
        teachers_paginate = Teacher.query.filter(Teacher.name.contains(search_query))

    # 添加分页功能
    page = request.args.get('page', 1, type=int)
    per_page = 10
    teachers_paginate = teachers_paginate.paginate(page=page, per_page=per_page, error_out=False)

    # 调试：输出查找到的教师数量
    print(f"Found {len(teachers_paginate.items)} teachers with the ID or Name '{search_query}'")
    
    return render_template('teachers_info.html', teachers=teachers_paginate.items, pagination=teachers_paginate)
