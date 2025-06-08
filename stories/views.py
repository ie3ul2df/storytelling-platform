from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg
from .forms import RegisterForm
from .models import Story, Chapter, Rating
from .forms import StoryForm, ChapterForm


# -----------------------------------------------

def story_list(request):
    stories = Story.objects.filter(is_public=True).order_by('-created_on')
    return render(request, 'stories/story_list.html', {'stories': stories})

# -----------------------------------------------

def story_detail(request, story_id):
    story = get_object_or_404(Story, id=story_id, is_public=True)

    # Get all root chapters (parent=None)
    root_chapters = story.chapters.filter(parent=None).order_by('created_on')
    branches = []
    for root in root_chapters:
        children = root.children.all()
        # Annotate children with average rating
        rated_children = children.annotate(avg_rating=Avg('ratings__value'))
        main_child = rated_children.order_by('-avg_rating').first() if children else None
        branches.append({
            'parent': root,
            'main': main_child,
            'alternatives': children,
        })

    return render(request, 'stories/story_detail.html', {
        'story': story,
        'branches': branches,
    })

# -----------------------------------------------

@login_required
def story_create(request):
    if request.method == 'POST':
        form = StoryForm(request.POST)
        chapter_title = request.POST.get('chapter_title')
        chapter_content = request.POST.get('chapter_content')

        if form.is_valid() and chapter_title and chapter_content:
            story = form.save(commit=False)
            story.author = request.user
            story.save()

            # Create first chapter
            Chapter.objects.create(
                story=story,
                title=chapter_title,
                content=chapter_content,
                author=request.user
            )
            return redirect('story_detail', story_id=story.id)
    else:
        form = StoryForm()
    return render(request, 'stories/story_form.html', {'form': form})

# -----------------------------------------------

@login_required
def chapter_create(request, story_id):
    story = get_object_or_404(Story, id=story_id, is_public=True)
    parent_id = request.GET.get('parent')
    parent_chapter = None
    if parent_id:
        parent_chapter = get_object_or_404(Chapter, id=parent_id, story=story)

    if not story.allow_contributions and request.user != story.author:
        return redirect('story_detail', story_id=story.id)

    if request.method == 'POST':
        form = ChapterForm(request.POST)
        if form.is_valid():
            chapter = form.save(commit=False)
            chapter.story = story
            chapter.author = request.user
            chapter.parent = parent_chapter
            chapter.save()
            return redirect('story_detail', story_id=story.id)
    else:
        form = ChapterForm()

    return render(request, 'stories/chapter_form.html', {
        'form': form,
        'story': story,
        'parent': parent_chapter,
    })

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
    user = request.user
    user_stories = user.story_set.all().order_by('-created_on')  # assuming related_name is default
    return render(request, 'stories/profile.html', {
        'user_profile': user,
        'user_stories': user_stories
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