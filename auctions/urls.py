from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createlisting", views.createlisting, name="createlisting"),
    path("listing/<str:title>", views.listing, name="listing"),
    path("remove/<str:title>", views.remove, name="remove"),
    path("add/<str:title>", views.add, name="add")
]
