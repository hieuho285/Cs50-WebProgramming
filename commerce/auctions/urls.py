from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create"),
    path("listing/<str:id>", views.listing, name="listing"),
    path("watchlist/<str:user_id>", views.watchlist, name="watchlist"),
    path("bid/<str:id>", views.bid, name="bid"),
    path("close/<str:id>", views.close, name="close"),
    path("comment/<str:id>", views.comment, name="comment"),
    path("category", views.category, name="category")
]
