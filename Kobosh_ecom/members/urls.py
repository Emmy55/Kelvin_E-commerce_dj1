from django.urls import path
from . import views

app_name = 'members'

urlpatterns = [
    path('', views.login_user, name='login_user'),
    path('signup_user/', views.signup_user, name='signup_user'),
    path('forgotpass/', views.forgotpass, name='forgotpass'),
]
