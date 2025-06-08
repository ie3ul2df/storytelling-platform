# FILE: stories/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.story_list, name='story_list'),
    path('story/<int:story_id>/', views.story_detail, name='story_detail'),
    path('story/new/', views.story_create, name='story_create'),
    path("<int:story_id>/chapter/create/", views.chapter_create, name="chapter_create"),
    path("<int:story_id>/season/create/", views.season_create, name="season_create"),
    path('chapter/<int:chapter_id>/edit/', views.chapter_edit, name='chapter_edit'),
    path('story/<int:story_id>/edit/', views.story_edit, name='story_edit'),
    path('chapter/<int:chapter_id>/delete/', views.chapter_delete, name='chapter_delete'),
    path('story/<int:story_id>/delete/', views.story_delete, name='story_delete'),
    path('accounts/profile/', views.profile_view, name='profile'),
    path('ajax/rate/', views.ajax_rate_chapter, name='ajax_rate_chapter'),
    path('test/', views.test_template, name='test_template'),
]
