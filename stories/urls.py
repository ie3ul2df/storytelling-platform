# FILE: stories/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.story_list, name='story_list'),
    path('story/<int:story_id>/', views.story_detail, name='story_detail'),
    path('story/new/', views.story_create, name='story_create'),
    path('story/<int:story_id>/add-chapter/', views.chapter_create, name='chapter_create'),
]
