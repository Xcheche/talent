from django.urls import path
from .import views


urlpatterns = [
    path('register/', views.register, name='register'),
    path('verify_account/', views.verify_account, name='verify_account'),
    path('', views.home, name='home'),
    #path('login/', views.login, name='login'),
]