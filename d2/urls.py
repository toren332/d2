from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from profiles import views

urlpatterns = [
    path('api/v0/users/',views.ProfileList.as_view()),
    path('api/v0/users/<int:user_id>/', views.ProfileDetail.as_view()),
    path('admin/', admin.site.urls),
    url(r'^api/v0/token-auth/', views.CustomAuthToken.as_view()),
    url(r'^api/v0/token-unauth/', views.UnAuth.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
