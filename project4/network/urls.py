
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),


    #API routes
    path("newpost", views.new_post, name="newpost"),
    path("showallpost", views.showallpost, name="showallpost"),
    path("showprofile/<str:user>", views.showprofile, name="showprofile"),
    path("updatelike/<int:post_id>", views.updatelike, name="updatelike"),
    path("follow/<str:user>", views.follow, name="follow"),
    path("updatefollow/<str:user>", views.updatefollow, name="updatefollow"),
    path("following/<str:user>", views.following, name="following"),

]
