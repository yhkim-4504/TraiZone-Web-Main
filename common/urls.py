from django.urls import path
from django.contrib import auth
from . import views

app_name = 'common'

urlpatterns = [
    path('login/', auth.views.LoginView.as_view(template_name='common/login.html'), name='login'),
    path('logout/', auth.views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
]