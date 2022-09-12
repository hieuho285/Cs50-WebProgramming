from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("search", views.search, name="search"),
    path("newpage", views.newpage, name="newpage"),
    path("edit", views.edit, name="edit"),
    path("newcontent", views.newcontent, name="newcontent"),
    path("random", views.random, name="random"),
]
