from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import F, Q, Avg
from django.core.paginator import Paginator
from django.urls import reverse
import json
from collections import defaultdict
from .forms import RegisterForm
from .models import Story, Chapter, Rating, UserProfile, StoryRating, Bookmark, Comment
from .forms import StoryForm, ChapterForm, UserProfileForm, CommentForm


# -----------------------------------------------
# ------------------ View to list stories with filters, sorting, pagination, and bookmark status


def story_list(request):
    query = request.GET.get("q", "").strip()
    author = request.GET.get("author", "").strip()
    min_rating = request.GET.get("min_rating", "").strip()
    sort = request.GET.get("sort", "top")

    # Base queryset with avg_rating annotation
    stories_qs = Story.objects.filter(is_public=True).annotate(
        avg_rating=Avg("ratings__value")
    )

    # Filters
    if query:
        stories_qs = stories_qs.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
    if author:
        stories_qs = stories_qs.filter(author__username__icontains=author)
    if min_rating.isdigit():
        stories_qs = stories_qs.filter(avg_rating__gte=float(min_rating))

    # Sorting
    if sort == "newest":
        stories_qs = stories_qs.order_by("-created_on")
    elif sort == "oldest":
        stories_qs = stories_qs.order_by("created_on")
    else:  # top ranked, unrated last
        stories_qs = stories_qs.order_by(F("avg_rating").desc(nulls_last=True))

    # Pagination
    paginator = Paginator(stories_qs, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Now that page_obj exists, get bookmarked IDs
    bookmarked_story_ids = set()
    if request.user.is_authenticated:
        bookmarked_story_ids = set(
            Bookmark.objects.filter(
                user=request.user, story__in=page_obj.object_list
            ).values_list("story_id", flat=True)
        )

    # Preserve other GET params in pagination links
    params = request.GET.copy()
    params.pop("page", None)

    return render(
        request,
        "stories/story_list.html",
        {
            "page_obj": page_obj,
            "params": params.urlencode(),
            "query": query,
            "author": author,
            "min_rating": min_rating,
            "sort": sort,
            "bookmarked_story_ids": bookmarked_story_ids,
        },
    )


# -----------------------------------------------
# ------------------ View to show story details, chapters, ratings, comments, and user interactions


def story_detail(request, story_id):
    story = get_object_or_404(Story, id=story_id, is_public=True)
    comment_id = request.GET.get("read_comment")
    if comment_id:
        try:
            comment = Comment.objects.get(id=comment_id)
            if (comment.story and comment.story.author == request.user) or (
                comment.chapter and comment.chapter.story.author == request.user
            ):
                comment.is_read = True
                comment.save()
        except Comment.DoesNotExist:
            pass
    comment_form = CommentForm()
    comments = story.comments.filter(parent=None)
    root_chapters = story.chapters.filter(parent=None).order_by("created_on")
    branches = []

    is_bookmarked = False
    if request.user.is_authenticated:
        is_bookmarked = story.bookmarked_by.filter(user=request.user).exists()

    is_following_author = False
    if request.user.is_authenticated:
        current_profile = request.user.userprofile
        author_profile = story.author.userprofile
        if current_profile != author_profile:
            is_following_author = current_profile.is_following(author_profile)

    for root in root_chapters:
        children = list(root.children.all().annotate(avg_rating=Avg("ratings__value")))

        root.avg_rating = root.average_rating
        if request.user.is_authenticated:
            root.user_rating = Rating.objects.filter(
                chapter=root, user=request.user
            ).first()

        for ch in children:
            ch.rating_count = ch.ratings.count()
            if request.user.is_authenticated:
                ch.user_rating = Rating.objects.filter(
                    chapter=ch, user=request.user
                ).first()

        sorted_chapters = sorted(
            [root] + children, key=lambda c: c.avg_rating or 0, reverse=True
        )

        branches.append(
            {
                "parent": root,
                "sorted_chapters": sorted_chapters,
            }
        )

    original_chapter = story.chapters.order_by("created_on").first()

    # --- Story-level user rating ---
    story_user_rating = 0
    if request.user.is_authenticated:
        obj = StoryRating.objects.filter(story=story, user=request.user).first()
        if obj:
            story_user_rating = obj.value  # .value should be an int field

    # Group chapters by index across all branches
    grouped_chapters = defaultdict(list)

    for branch in branches:
        for i, chapter in enumerate(branch["sorted_chapters"], start=1):
            grouped_chapters[i].append(chapter)

    # Optional: Convert defaultdict to regular dict (cleaner in templates)
    grouped_chapters = dict(grouped_chapters)

    return render(
        request,
        "stories/story_detail.html",
        {
            "story": story,
            "branches": branches,
            "original_chapter": original_chapter,
            "story_user_rating": story_user_rating,
            "is_bookmarked": is_bookmarked,
            "is_following_author": is_following_author,
            "comment_form": comment_form,
            "comments": comments,
        },
    )


# -----------------------------------------------
# ------------------ View to create a new story (login required)


@login_required
def story_create(request):
    if request.method == "POST":
        form = StoryForm(request.POST, request.FILES)
        if form.is_valid():
            story = form.save(commit=False)
            story.author = request.user
            story.save()
            return redirect("profile")  # or wherever you want
    else:
        form = StoryForm()

    return render(request, "stories/story_form.html", {"form": form})


# -----------------------------------------------
# ------------------ View to create a chapter (optionally as a child), login required


@login_required
def chapter_create(request, story_id):
    story = get_object_or_404(Story, pk=story_id)
    parent_id = request.GET.get("parent")
    parent = get_object_or_404(Chapter, pk=parent_id) if parent_id else None

    if request.method == "POST":
        form = ChapterForm(request.POST)
        if form.is_valid():
            chapter = form.save(commit=False)
            chapter.story = story
            chapter.parent = parent
            chapter.author = request.user
            chapter.save()
            return redirect("story_detail", story_id=story.id)
    else:
        form = ChapterForm()

    return render(request, "stories/chapter_form.html", {"form": form, "story": story})


# -----------------------------------------------
# ------------------ View to create a new root chapter (season), with permission check


@login_required
def season_create(request, story_id):
    story = get_object_or_404(Story, pk=story_id)

    if not (story.allow_contributions or story.author == request.user):
        return redirect("story_detail", story_id=story.id)

    if request.method == "POST":
        form = ChapterForm(request.POST)
        if form.is_valid():
            chapter = form.save(commit=False)
            chapter.story = story
            chapter.parent = None  # Root chapter (new season)
            chapter.author = request.user
            chapter.save()
            return redirect("story_detail", story_id=story.id)
    else:
        form = ChapterForm()

    return render(
        request,
        "stories/chapter_form.html",
        {"form": form, "story": story, "new_season": True},
    )


# -----------------------------------------------
# ------------------ View to register and log in a new user


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("story_list")
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form": form})


# -----------------------------------------------
# ------------------ View for user profile: edit info, list stories, bookmarks, and unread comments


@login_required
def profile_view(request):
    user = request.user
    profile = user.userprofile

    # Fetch unread comments on your stories or chapters
    unread_comments = Comment.objects.filter(
        Q(story__author=user) | Q(chapter__story__author=user), is_read=False
    )

    search_query = request.GET.get("search", "")
    sort_by = request.GET.get("sort", "created_on")

    stories = Story.objects.filter(author=user)
    bookmarks = Bookmark.objects.filter(user=user).select_related("story")

    if search_query:
        stories = stories.filter(title__icontains=search_query)

    if sort_by == "-average_rating":
        stories = stories.annotate(avg_rating=Avg("chapters__ratings__value")).order_by(
            "-avg_rating"
        )
    else:
        stories = stories.order_by("-created_on")

    form = UserProfileForm(
        request.POST or None, request.FILES or None, instance=profile
    )
    if request.method == "POST" and form.is_valid():
        form.save()

    context = {
        "profile": profile,
        "user_stories": stories,
        "profile_form": form,
        "bookmarks": bookmarks,
        "following": profile.following.all(),
        "followers": profile.followers.all(),
        "sort": sort_by,
        "unread_comments": unread_comments,
    }

    return render(request, "stories/profile.html", context)


# -----------------------------------------------
# ------------------ View to edit a chapter (only by its author)


@login_required
def chapter_edit(request, chapter_id):
    chapter = get_object_or_404(Chapter, id=chapter_id)
    if request.user != chapter.author:
        return redirect("story_detail", story_id=chapter.story.id)

    if request.method == "POST":
        form = ChapterForm(request.POST, instance=chapter)
        if form.is_valid():
            form.save()
            return redirect("story_detail", story_id=chapter.story.id)
    else:
        form = ChapterForm(instance=chapter)

    return render(
        request,
        "stories/chapter_form.html",
        {
            "form": form,
            "story": chapter.story,
            "parent": chapter.parent,
        },
    )


# -----------------------------------------------
# ------------------ View to delete a chapter (only by its author)


@login_required
def chapter_delete(request, chapter_id):
    chapter = get_object_or_404(Chapter, id=chapter_id)
    if request.user == chapter.author:
        story_id = chapter.story.id
        chapter.delete()
        return redirect("story_detail", story_id=story_id)
    return redirect("story_detail", story_id=chapter.story.id)


# -----------------------------------------------
# ------------------ Handle AJAX POST to rate a chapter (create or update)


@require_POST
@login_required
def rate_chapter(request):
    try:
        data = json.loads(request.body)
        chapter_id = data.get("chapter_id")
        rating_value = int(data.get("rating"))

        chapter = Chapter.objects.get(id=chapter_id)
        rating, created = Rating.objects.update_or_create(
            chapter=chapter, user=request.user, defaults={"value": rating_value}
        )

        return JsonResponse({"success": True, "rating": rating_value})

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


# -----------------------------------------------
# ------------------ Handle form-encoded AJAX POST to rate a chapter and return new average


@require_POST
@login_required
def ajax_rate_chapter(request):
    try:
        chapter_id = int(request.POST.get("chapter_id"))
        value = int(request.POST.get("value"))

        if not (1 <= value <= 5):
            return HttpResponseBadRequest("Invalid rating value")

        chapter = Chapter.objects.get(pk=chapter_id)
        Rating.objects.update_or_create(
            chapter=chapter, user=request.user, defaults={"value": value}
        )

        avg = chapter.average_rating  # optional: use .aggregate(Avg) if needed
        return JsonResponse({"success": True, "average": round(avg, 1)})

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


# -----------------------------------------------
# ------------------ View to edit a story (only by its author)


@login_required
def story_edit(request, story_id):
    story = get_object_or_404(Story, id=story_id, author=request.user)

    if request.method == "POST":
        form = StoryForm(request.POST, request.FILES, instance=story)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = StoryForm(instance=story)

    return render(request, "stories/story_edit.html", {"form": form, "story": story})


# -----------------------------------------------
# ------------------ View to delete a story (author only), with confirmation page


@login_required
def story_delete(request, story_id):
    story = get_object_or_404(Story, id=story_id, author=request.user)
    if request.method == "POST":
        story.delete()
        return redirect("profile")
    return render(request, "stories/story_confirm_delete.html", {"story": story})


# -----------------------------------------------
# ------------------ Handle AJAX POST to rate a story and return updated average


@require_POST
@login_required
def rate_story(request):
    try:
        data = json.loads(request.body)
        story_id = int(data.get("story_id"))
        value = int(data.get("rating"))

        if not (1 <= value <= 5):
            return HttpResponseBadRequest("Invalid rating")

        story = get_object_or_404(Story, pk=story_id)

        StoryRating.objects.update_or_create(
            story=story, user=request.user, defaults={"value": value}
        )

        avg = story.average_rating
        return JsonResponse({"success": True, "average": round(avg, 1)})

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


# -----------------------------------------------
# ------------------ AJAX handlers to bookmark or unbookmark a story


@login_required
@require_POST
def bookmark_story(request, story_id):
    story, created = Story.objects.get_or_create(id=story_id)
    Bookmark.objects.get_or_create(user=request.user, story=story)
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({"bookmarked": True, "story_id": story_id})
    return redirect("story_detail", story_id=story_id)


@login_required
@require_POST
def unbookmark_story(request, story_id):
    Bookmark.objects.filter(user=request.user, story_id=story_id).delete()
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({"bookmarked": False, "story_id": story_id})
    return redirect("story_detail", story_id=story_id)


# -----------------------------------------------


@login_required
@require_POST
def toggle_follow(request, username):
    target_user = get_object_or_404(User, username=username)
    target_profile = get_object_or_404(UserProfile, user=target_user)
    current_profile = request.user.userprofile

    # Prevent following yourself
    if current_profile == target_profile:
        return redirect(request.POST.get("next") or reverse("profile", args=[username]))

    if current_profile.is_following(target_profile):
        current_profile.following.remove(target_profile)
    else:
        current_profile.following.add(target_profile)

    # Redirect back to where the request came from (story detail or profile)
    return redirect(request.POST.get("next") or reverse("profile", args=[username]))


# -----------------------------------------------
# ------------------ Toggle follow/unfollow for another user's profile


@login_required
def public_profile_view(request, username):
    target_user = get_object_or_404(User, username=username)

    # Redirect to own profile if user tries to access their own public URL
    if request.user.username == target_user.username:
        return redirect("profile")

    profile = get_object_or_404(UserProfile, user=target_user)
    is_following = request.user.userprofile.is_following(profile)

    public_stories = Story.objects.filter(author=target_user, is_public=True)
    chapters_count = Chapter.objects.filter(story__author=target_user).count()

    context = {
        "profile": profile,
        "user_stories": public_stories,
        "chapters_count": chapters_count,
        "followers": profile.followers.all(),
        "following": profile.following.all(),
        "is_following": is_following,
    }

    return render(request, "stories/public_profile.html", context)


# -----------------------------------------------
# ------------------ Add, edit, or delete comments on stories/chapters (login required)


@login_required
@require_POST
def add_comment(request, story_id=None, chapter_id=None):
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user

        parent_id = request.POST.get("parent_id")
        if parent_id:
            comment.parent = Comment.objects.get(id=parent_id)

        # SAFELY HANDLE STORY OR CHAPTER
        if story_id:
            try:
                comment.story = Story.objects.get(id=story_id)
            except Story.DoesNotExist:
                return HttpResponseBadRequest("Story not found")
        elif chapter_id:
            try:
                comment.chapter = Chapter.objects.get(id=chapter_id)
            except Chapter.DoesNotExist:
                return HttpResponseBadRequest("Chapter not found")
        else:
            return HttpResponseBadRequest("Missing story or chapter ID")

        comment.save()
        return redirect(request.META.get("HTTP_REFERER", "/"))
    return HttpResponseBadRequest("Invalid comment form")


@login_required
@require_POST
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    form = CommentForm(request.POST, instance=comment)
    if form.is_valid():
        form.save()
    return redirect(request.META.get("HTTP_REFERER", "/"))


@login_required
@require_POST
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    comment.delete()
    return redirect(request.META.get("HTTP_REFERER", "/"))
