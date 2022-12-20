from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_user, name="login"),
    path("logout", views.logout_user, name="logout"),
    path("timer", views.timer, name="timer"),
    path("config", views.config, name="config"),
]