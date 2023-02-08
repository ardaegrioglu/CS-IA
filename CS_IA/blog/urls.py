from . import views
from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('', views.index, name='index'),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),
    path("read/<int:id>", views.article, name="article"),
    path("history/", views.history, name="history"),
    path("favorite/<int:id>", views.favoriteapi, name="favoriteapi"),
    path("favorites/", views.favorite, name="favorites"),
    path("unfavorite/<int:id>", views.unfavoriteapi, name="unfavoriteapi"),
    path("create/", views.create, name="create"),
    path("edit/", views.edit, name="edit"),
    path("delete/", views.delete, name="delete"),
    path("deleteapi/<int:id>", views.deleteapi, name="deleteapi"),
    path("editblog/<int:id>", views.editblog, name="editblog"),
    path("visualise/", views.visualise, name="visualise"),
    path('api', views.ChartData.as_view()),
    path('logoutapi', views.logoutapi, name="logoutapi"),
]
