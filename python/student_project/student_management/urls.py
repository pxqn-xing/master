# student_management/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),                  # 登录接口
    path('get_student_info/', views.get_student_info, name='get_student_info'),  # 获取学生信息接口
]
