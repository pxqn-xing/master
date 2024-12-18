from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..models import User, db
from datetime import datetime
from sqlalchemy.orm import aliased
from sqlalchemy import or_

root_bp = Blueprint('root', __name__)

# 管理员列表 (现在显示的是 User 数据)
@root_bp.route('/admins/', methods=['GET'])
def admins_list():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    # 查询 User 数据而不是 Root 数据
    admins_paginate = User.query.paginate(page=page, per_page=per_page, error_out=False)
    return render_template('admins_info.html', admins=admins_paginate.items, pagination=admins_paginate)


# 编辑管理员信息 (编辑 User 数据)
@root_bp.route('/admins/edit/<int:admin_id>', methods=['GET', 'POST'])
def edit_admin(admin_id):
    admin = User.query.get_or_404(admin_id)  # 获取 User 数据
    if request.method == 'POST':
        # 只允许修改普通管理员的用户名和密码
        if admin.username != 'superadmin':  # 确保不能修改超级管理员账户
            admin.username = request.form['username']
            password = request.form['password']
            if password:
                admin.password = password  # 如果密码有更新，则修改密码

            try:
                db.session.commit()
                flash("管理员信息更新成功！", "success")
                return redirect(url_for('root.admins_list'))
            except Exception as e:
                db.session.rollback()
                flash(f"更新失败，错误信息：{e}", "danger")
                return redirect(url_for('root.edit_admin', admin_id=admin.id))
        else:
            flash("不能修改超级管理员账户信息", "danger")
            return redirect(url_for('root.admins_list'))

    return render_template('edit_admin.html', admin=admin)


# 删除管理员 (删除 User 数据)
@root_bp.route('/admins/delete/<int:admin_id>', methods=['GET'])
def delete_admin(admin_id):
    admin = User.query.get_or_404(admin_id)  # 获取 User 数据
    try:
        db.session.delete(admin)
        db.session.commit()
        flash("管理员删除成功！", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"删除失败，错误信息：{e}", "danger")

    return redirect(url_for('root.admins_list'))


# 搜索管理员 (按 User 数据进行搜索)
@root_bp.route('/admins/search', methods=['GET'])
def search_admins():
    search_query = request.args.get('query', '').strip()
    if not search_query:
        flash("请输入搜索内容", "warning")
        return redirect(url_for('root.admins_list'))

    # 如果是数字，按管理员ID查找；如果是字符串，按用户名查找
    if search_query.isdigit():
        admins_paginate = User.query.filter(User.id == int(search_query))  # 按 ID 查找
    else:
        admins_paginate = User.query.filter(
            or_(
                User.username.contains(search_query),  # 按用户名查找
            )
        )

    # 添加分页功能
    page = request.args.get('page', 1, type=int)
    per_page = 10
    admins_paginate = admins_paginate.paginate(page=page, per_page=per_page, error_out=False)

    return render_template('admins_info.html', admins=admins_paginate.items, pagination=admins_paginate)
