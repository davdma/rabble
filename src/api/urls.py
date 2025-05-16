from django.urls import path

from . import views

urlpatterns = [
    path('subrabbles/', views.subrabble_list, name='subrabble_list'),
    path('subrabbles/!<str:identifier>/', views.subrabble_detail, name='subrabble_detail'),
    path('subrabbles/!<str:identifier>/posts/', views.post_list, name='post_list'),
    path('subrabbles/!<str:identifier>/posts/<int:pk>/', views.post_detail, name='post_detail'),
    path('subrabbles/!<str:identifier>/posts/<int:pk>/likes/', views.post_like, name='post_like')
]