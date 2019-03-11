from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from profiles import views

urlpatterns = [
    path('api/v0/groups/',views.GroupList.as_view()),
    path('api/v0/users/',views.UserList.as_view()),
    path('api/v0/users/teachers',views.TeacherList.as_view()),
    path('api/v0/users/students',views.StudentList.as_view()),
    path('api/v0/users/teachers/<int:user_id>/', views.TeacherDetail.as_view()),
    path('api/v0/users/students/<int:user_id>/', views.StudentDetail.as_view()),
    path('admin/', admin.site.urls),
    url(r'^api/v0/auth/', views.CustomAuthToken.as_view()),
    url(r'^api/v0/unauth/', views.UnAuth.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
