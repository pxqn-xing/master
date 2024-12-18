from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app)

    # 应用配置
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:040712@localhost/students_inf'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = os.urandom(24)

    db.init_app(app)

    # 注册蓝图
    from .routes.auth import auth_bp
    from .routes.student import student_bp
    from .routes.teacher import teacher_bp
    from .routes.course import course_bp
    from .routes.grade import grade_bp
    from .routes.root import root_bp  # 根路由在这里导入

    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(teacher_bp)
    app.register_blueprint(course_bp)
    app.register_blueprint(grade_bp)
    app.register_blueprint(root_bp)

    return app
