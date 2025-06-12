# FILE: stories/urls.py

from django.urls import path
from . import views

# ------------------ URL routes for stories, chapters, ratings, bookmarks, profiles, and comments

urlpatterns = [
    path("", views.story_list, name="story_list"),
    path("story/<int:story_id>/", views.story_detail, name="story_detail"),
    path("story/new/", views.story_create, name="story_create"),
    path("<int:story_id>/chapter/create/", views.chapter_create, name="chapter_create"),
    path("<int:story_id>/season/create/", views.season_create, name="season_create"),
    path("chapter/<int:chapter_id>/edit/", views.chapter_edit, name="chapter_edit"),
    path("story/<int:story_id>/edit/", views.story_edit, name="story_edit"),
    path(
        "chapter/<int:chapter_id>/delete/", views.chapter_delete, name="chapter_delete"
    ),
    path("story/<int:story_id>/delete/", views.story_delete, name="story_delete"),
    path("ajax/rate/", views.ajax_rate_chapter, name="ajax_rate_chapter"),
    path("rate-story/", views.rate_story, name="rate_story"),
    path(
        "stories/<int:story_id>/bookmark/", views.bookmark_story, name="bookmark_story"
    ),
    path(
        "stories/<int:story_id>/unbookmark/",
        views.unbookmark_story,
        name="unbookmark_story",
    ),
    path(
        "profile/<str:username>/toggle-follow/",
        views.toggle_follow,
        name="toggle_follow",
    ),
    path("profile/", views.profile_view, name="profile"),
    path("profile/<str:username>/", views.public_profile_view, name="public_profile"),
    path(
        "stories/<int:story_id>/comment/", views.add_comment, name="add_story_comment"
    ),
    path(
        "stories/<int:story_id>/comment/", views.add_comment, name="add_story_comment"
    ),
    path(
        "chapters/<int:chapter_id>/comment/",
        views.add_comment,
        name="add_chapter_comment",
    ),
    path("comment/<int:comment_id>/edit/", views.edit_comment, name="edit_comment"),
    path(
        "comment/<int:comment_id>/delete/", views.delete_comment, name="delete_comment"
    ),
]
