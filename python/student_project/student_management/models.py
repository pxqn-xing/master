# student_management/models.py

from django.db import models

class Student(models.Model):
    student_id = models.CharField(max_length=100, unique=True)  # 学号
    name = models.CharField(max_length=100)                      # 姓名
    email = models.EmailField()                                  # 邮箱
    password = models.CharField(max_length=100)                  # 密码（建议加密存储）

    def __str__(self):
        return self.name
