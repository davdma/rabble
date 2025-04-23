from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("profile", views.profile, name="profile"),
    path("!<slug:identifier>/", views.subrabble_detail, name="subrabble-detail"),
    path("!<slug:identifier>/<int:pk>/", views.post_detail, name="post-detail"),
    path("!<slug:identifier>/new", views.post_create, name="post-create"),
    path("!<slug:identifier>/<int:pk>/edit", views.post_edit, name="post-edit")
]