from django.db import models
from django.contrib.auth.models import User
from model_utils import Choices
from rest_framework.authtoken.models import Token

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class Profile(models.Model):
    EMPLOYEE = Choices('teacher', 'student')
    employee = models.CharField(choices=EMPLOYEE, default=EMPLOYEE.student, max_length=7)
    good = models.CharField(name="good",max_length=20,blank=True,null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
