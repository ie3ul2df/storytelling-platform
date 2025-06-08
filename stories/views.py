from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
import json
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg, Count  
from .forms import RegisterForm, RatingForm
from .models import Story, Chapter, Rating, UserProfile
from .forms import StoryForm, ChapterForm, UserProfileForm
from . import models


# -----------------------------------------------

def test_template(request):
    return render(request, 'test.html')

# -----------------------------------------------

def story_list(request):
    stories = list(Story.objects.filter(is_public=True))

    # Sort by total_rank descending
    stories.sort(key=lambda s: s.total_rank or 0, reverse=True)

    return render(request, "stories/story_list.html", {"stories": stories})


# -----------------------------------------------

def story_detail(request, story_id):
    story = get_object_or_404(Story, id=story_id, is_public=True)

    root_chapters = story.chapters.filter(parent=None).order_by('created_on')
    branches = []

    for root in root_chapters:
        children = list(
            root.children.all().annotate(avg_rating=Avg("ratings__value"))
        )

        # Add the parent with avg_rating
        root.avg_rating = root.average_rating
        all_chapters = [root] + children

        # Add user rating and rating count
        for ch in all_chapters:
            ch.rating_count = ch.ratings.count()
            if request.user.is_authenticated:
                ch.user_rating = Rating.objects.filter(chapter=ch, user=request.user).first()

        # Sort combined list by avg_rating desc
        sorted_chapters = sorted(all_chapters, key=lambda c: c.avg_rating or 0, reverse=True)

        branches.append({
            'parent': root,  # keep for context if needed
            'sorted_chapters': sorted_chapters,
        })

    return render(request, 'stories/story_detail.html', {
        'story': story,
        'branches': branches,
    })



# -----------------------------------------------


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

    return render(request, "stories/chapter_form.html", {"form": form, "story": story, "new_season": True})
# -----------------------------------------------

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('story_list')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})

# -----------------------------------------------

@login_required
def profile_view(request):
    search_query = request.GET.get("search", "")
    sort_by = request.GET.get("sort", "created_on")

    stories = Story.objects.filter(author=request.user)

    if search_query:
        stories = stories.filter(title__icontains=search_query)

    if sort_by == "-average_rating":
        stories = stories.annotate(avg=models.Avg("chapters__ratings__value")).order_by("-avg")
    else:
        stories = stories.order_by("-created_on")

    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
    else:
        form = UserProfileForm(instance=request.user.userprofile)

    return render(request, "stories/profile.html", {
        "user_stories": stories,
        "profile_form": form
    })

# -----------------------------------------------

@login_required
def chapter_edit(request, chapter_id):
    chapter = get_object_or_404(Chapter, id=chapter_id)
    if request.user != chapter.author:
        return redirect('story_detail', story_id=chapter.story.id)

    if request.method == 'POST':
        form = ChapterForm(request.POST, instance=chapter)
        if form.is_valid():
            form.save()
            return redirect('story_detail', story_id=chapter.story.id)
    else:
        form = ChapterForm(instance=chapter)

    return render(request, 'stories/chapter_form.html', {
        'form': form,
        'story': chapter.story,
        'parent': chapter.parent,
    })

# -----------------------------------------------

@login_required
def chapter_delete(request, chapter_id):
    chapter = get_object_or_404(Chapter, id=chapter_id)
    if request.user == chapter.author:
        story_id = chapter.story.id
        chapter.delete()
        return redirect('story_detail', story_id=story_id)
    return redirect('story_detail', story_id=chapter.story.id)


# -----------------------------------------------

@require_POST
@login_required
def rate_chapter(request):
    try:
        data = json.loads(request.body)
        chapter_id = data.get('chapter_id')
        rating_value = int(data.get('rating'))

        chapter = Chapter.objects.get(id=chapter_id)
        rating, created = Rating.objects.update_or_create(
            chapter=chapter,
            user=request.user,
            defaults={'value': rating_value}
        )

        return JsonResponse({'success': True, 'rating': rating_value})

    except Exception as e:
        print("Error in rate_chapter:", e)
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

# -----------------------------------------------

@require_POST
@login_required
def ajax_rate_chapter(request):
    try:
        print("📥 RAW POST DATA:", request.body)
        print("📥 POST:", request.POST)

        chapter_id = int(request.POST.get("chapter_id"))
        value = int(request.POST.get("value"))

        if not (1 <= value <= 5):
            return HttpResponseBadRequest("Invalid rating value")

        chapter = Chapter.objects.get(pk=chapter_id)
        Rating.objects.update_or_create(
            chapter=chapter,
            user=request.user,
            defaults={'value': value}
        )


        avg = chapter.average_rating  # optional: use .aggregate(Avg) if needed
        return JsonResponse({"success": True, "average": round(avg, 1)})

    except Exception as e:
        print("🔥 ERROR:", e)
        return JsonResponse({"success": False, "error": str(e)}, status=500)

# -----------------------------------------------

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

@login_required
def story_delete(request, story_id):
    story = get_object_or_404(Story, id=story_id, author=request.user)
    if request.method == "POST":
        story.delete()
        return redirect("profile")
    return render(request, "stories/story_confirm_delete.html", {"story": story})

