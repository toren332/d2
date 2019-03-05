from django.db import models
from django.contrib.auth.models import User
from model_utils import Choices


class PrimaryLesson(models.Model):
    """Учебные уроки"""
    teacher = models.CharField(name="teacher", max_length=50,
                               help_text='Teacher name, like: Ivanov Ivan Ivanovich')
    KIND = Choices('lesson', 'lecture')
    name = models.CharField(name="name", max_length=50,
                            help_text='Lesson name, like: Math')
    lesson_kind = models.CharField(choices=KIND, default=KIND.lesson, max_length=7,
                                   help_text='Lesson kind: lesson or lecture; lesson is default')
    start_time = models.TimeField()
    end_time = models.TimeField()
    date = models.DateField()

    def __str__(self):
        return self.lesson_kind + ': ' + self.name


class PrimaryGroup(models.Model):
    """Учебная группа"""
    name = models.CharField(name="name", max_length=50,
                            help_text='Primary Group name, like:425')

    def __str__(self):
        return 'Group: ' + self.name


class PrimaryGroupPrimaryLesson(models.Model):
    primary_group = models.ForeignKey(PrimaryGroup, on_delete=models.CASCADE)
    primary_lesson = models.ForeignKey(PrimaryLesson, on_delete=models.CASCADE)


class Profile(models.Model):
    """Профиль пользователя."""
    KIND = Choices('teacher', 'student')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    primary_group = models.ForeignKey(PrimaryGroup, on_delete=models.CASCADE)

    account_kind = models.CharField(choices=KIND, default=KIND.student, max_length=7,
                                    help_text='Account kind: teacher or student; student is default')
    first_name = models.CharField('first name', max_length=40, blank=True,
                                  help_text='Account first name')
    middle_name = models.CharField('middle name', max_length=40, blank=True,
                                   help_text='Account middle name')
    last_name = models.CharField('last name', max_length=40, blank=True,
                                 help_text='Account last name')


    def __str__(self):
        return 'Login: ' + self.user.username
