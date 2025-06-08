# FILE: stories/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.story_list, name='story_list'),
    path('story/<int:story_id>/', views.story_detail, name='story_detail'),
    path('story/new/', views.story_create, name='story_create'),
    path('story/<int:story_id>/add-chapter/', views.chapter_create, name='chapter_create'),
    path('chapter/<int:chapter_id>/edit/', views.chapter_edit, name='chapter_edit'),
    path('chapter/<int:chapter_id>/delete/', views.chapter_delete, name='chapter_delete'),
    path('accounts/profile/', views.profile_view, name='profile'),
    path('ajax/rate/', views.ajax_rate_chapter, name='ajax_rate_chapter'),
]
