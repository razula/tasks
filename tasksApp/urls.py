from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.loginUser, name="login"),
    path("logout/", views.logout, name="logout"),
    path("signup/", views.signup, name="signup"),
    path("add/task/", views.addTask, name="addTask"),
    path("update/task/", views.updateTask, name="updateTask"),
    path("delete/task/", views.deleteTask, name="deleteTask"),
    path("api/users/", views.usersAPI, name="usersAPI"),
    path("delete/users/", views.deleteUsers, name="deleteUsers"),
    path("api/session/", views.sessionAPI, name="sessionAPI"),
    path("api/tasks/", views.tasksAPI, name="tasksAPI"),
    ]

