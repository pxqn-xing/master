from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from ..models import User, db,Root

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/select_role', methods=['GET', 'POST'])
def select_role():
    if request.method == 'POST':
        # 获取用户选择的角色
        role = request.form.get('role')
        if role == 'admin':
            return render_template('login.html')  # 返回管理员登录页面
        elif role == 'super_admin':
            return render_template('login_superadmin.html')  # 返回超级管理员登录页面
    return render_template('select_role.html')  # 如果是 GET 请求，则显示角色选择页面

@auth_bp.route('/', methods=['GET', 'POST'])
def index():
    return redirect(url_for('auth.select_role'))  # 默认跳转到身份选择页面


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not username or not password or not confirm_password:
            flash("所有字段均为必填项", "danger")
            return redirect(url_for('auth.register'))

        if password != confirm_password:
            flash("密码不匹配，请重新输入", "danger")
            return redirect(url_for('auth.register'))

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("用户名已存在，请选择其他用户名", "danger")
            return redirect(url_for('auth.register'))

        new_user = User(username=username, password=password)

        try:
            db.session.add(new_user)
            db.session.commit()
            flash(f"注册成功！用户名 {username} 已存入数据库。请登录", "success")
            return redirect(url_for('auth.index'))  # 注册成功后跳转到登录页面
        except Exception as e:
            db.session.rollback()
            flash(f"注册失败，请稍后再试。错误信息: {e}", "danger")
            return redirect(url_for('auth.register'))

    return render_template('register.html')

# 登录逻辑
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.json.get('username')
        password = request.json.get('password')
        role = request.json.get('role')

        if not username or not password or not role:
            return jsonify({'success': False, 'message': '用户名、密码和角色均为必填项'}), 400

        if role == 'admin':
            user = User.query.filter_by(username=username).first()
            if user and user.password == password:
                session['user_id'] = user.id
                session['username'] = user.username
                session['role'] = 'admin'
                return jsonify({'success': True, 'message': '管理员登录成功', 'role': 'admin'}), 200

        elif role == 'superadmin':
            superadmin = Root.query.filter_by(username=username).first()
            if superadmin and superadmin.password == password:
                session['user_id'] = superadmin.id
                session['username'] = superadmin.username
                session['role'] = 'superadmin'
                return jsonify({'success': True, 'message': '超级管理员登录成功', 'role': 'superadmin'}), 200

        return jsonify({'success': False, 'message': '用户名或密码错误'}), 401
    else:
        # 如果是 GET 请求，返回登录页面（或者跳转到其它页面）
        return render_template('login.html')


@auth_bp.route('/login_superadmin', methods=['GET', 'POST'])
def login_superadmin():
    return render_template('login_superadmin.html')


@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash("您已成功注销", "info")
    return redirect(url_for('auth.index'))
