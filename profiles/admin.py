from django.contrib import admin
from .models import Profile, PrimaryGroup, PrimaryLesson, PrimaryGroupPrimaryLesson

admin.site.register(Profile)
admin.site.register(PrimaryGroup)
admin.site.register(PrimaryLesson)
admin.site.register(PrimaryGroupPrimaryLesson)
