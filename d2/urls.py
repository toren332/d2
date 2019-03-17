from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from profiles import views
from profiles.views import Users, Groups, Students, Teachers, StudentsGroups
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('api/v0/users', Users, basename='user')
router.register('api/v0/groups', Groups, basename='group')
router.register('api/v0/teachers', Teachers, basename='teacher')
router.register('api/v0/students', Students, basename='student')
router.register('api/v0/students_groups', StudentsGroups, basename='student_group')


urlpatterns = router.urls

urlpatterns += [
    path(r'admin/', admin.site.urls),
    url(r'^api/v0/users/auth/login', views.Auth.as_view()),
    url(r'^api/v0/users/auth/logout', views.UnAuth.as_view()),

]
'''
path('api/v0/groups/',views.GroupList.as_view()),
path('api/v0/users/',views.UserList.as_view()),
path('api/v0/users/teachers/',views.TeacherList.as_view()),
path('api/v0/users/students/',views.StudentList.as_view()),
path('api/v0/users/teachers/<int:user_id>/', views.TeacherDetail.as_view()),
path('api/v0/users/students/<int:user_id>/', views.StudentDetail.as_view()),
path('api/v0/users/students/<int:user_id>/groups/', views.StudentSetGroup.as_view()),

url(r'^api/v0/auth/', views.CustomAuthToken.as_view()),
url(r'^api/v0/unauth/', views.UnAuth.as_view()),
'''
