from django.db import models
from django.contrib.auth.models import User


class Teacher(models.Model):
    """Профиль преподавателя."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    first_name = models.CharField('first_name', max_length=40, blank=True,
                                  help_text='Account first name')
    middle_name = models.CharField('middle_name', max_length=40, blank=True,
                                   help_text='Account middle name')
    last_name = models.CharField('middle_name', max_length=40, blank=True,
                                 help_text='Account last name')
    is_verified = models.BooleanField('is_verified', default=False,
                                      help_text='Indicates teacher has been verified for identity')

    def __str__(self):
        return 'Login: ' + self.user.username


class Group(models.Model):
    """Группа."""
    name = models.CharField('name', max_length=40, blank=True,
                            help_text='Group name')
    is_primary = models.BooleanField('is_primary', default=False,
                                     help_text='Indicates is the group primary')

    def __str__(self):
        return 'Group: ' + self.name + '; verified: ' + str(self.is_primary)


class Student(models.Model):
    """Профиль студента."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    first_name = models.CharField('first name', max_length=40, blank=True,
                                  help_text='Account first name')
    middle_name = models.CharField('middle name', max_length=40, blank=True,
                                   help_text='Account middle name')
    last_name = models.CharField('last name', max_length=40, blank=True,
                                 help_text='Account last name')

    def __str__(self):
        return 'Login: ' + self.user.username


class StudentGroup(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
