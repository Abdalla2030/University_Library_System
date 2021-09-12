from django.urls import path
from . import views

# from django.contrib.auth.views import login, logout

urlpatterns = [
    path('admin/signup/', views.signupAdmin, name='admin-signup'),
    path('admin/login/', views.loginAdmin, name='admin-login'),
    path('student/signup/', views.signupStudent, name='student-signup'),
    path('student/login/', views.loginStudent, name='student-login'),
    path('logout/', views.userLogout, name='logout')
]
