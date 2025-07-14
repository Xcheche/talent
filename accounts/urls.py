from django.urls import path
from . import views


urlpatterns = [
    path("register/", views.register, name="register"),
    path("verify_account/", views.verify_account, name="verify_account"),
    path("login/", views.login, name="login"),
    path("", views.home, name="home"),
    path("logout/", views.logout, name="logout"),
    # path('login/', views.login, name='login'),
]
