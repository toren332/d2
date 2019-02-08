from django.db import models
from django.contrib.auth.models import User
from model_utils import Choices



class Profile(models.Model):
    EMPLOYEE = Choices('teacher', 'student')
    employee = models.CharField(choices=EMPLOYEE, default=EMPLOYEE.student, max_length=7)
    good = models.CharField(name="good",max_length=20,blank=True,null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
