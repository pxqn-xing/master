# student_management/views.py

from django.http import JsonResponse
from django.contrib.auth.hashers import check_password
from .models import Student

# 用户登录视图
def login(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        password = request.POST.get('password')

        try:
            student = Student.objects.get(student_id=student_id)
            if check_password(password, student.password):  # 验证密码
                # 登录成功
                return JsonResponse({'status': 'success', 'message': '登录成功', 'student_name': student.name})
            else:
                return JsonResponse({'status': 'error', 'message': '密码错误'})
        except Student.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': '学生不存在'})

    return JsonResponse({'status': 'error', 'message': '请求方式错误'})

# 获取学生信息视图
def get_student_info(request):
    if request.method == 'GET':
        students = Student.objects.all().values('student_id', 'name', 'email')
        student_list = list(students)  # 转换为列表格式返回
        return JsonResponse({'status': 'success', 'students': student_list})
    return JsonResponse({'status': 'error', 'message': '请求方式错误'})
