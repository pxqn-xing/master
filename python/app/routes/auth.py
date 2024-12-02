from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from ..models import User, db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    return render_template('login.html')

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

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': '未接收到数据'}), 400

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'success': False, 'message': '用户名和密码均为必填项'}), 400

    user = User.query.filter_by(username=username).first()
    if user and user.password == password:
        session['user_id'] = user.id
        session['username'] = user.username
        return jsonify({'success': True, 'message': '登录成功', 'username': user.username}), 200

    return jsonify({'success': False, 'message': '用户名或密码错误'}), 401

@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash("您已成功注销", "info")
    return redirect(url_for('auth.index'))
