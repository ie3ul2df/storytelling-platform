from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Story
from .forms import StoryForm

def story_list(request):
    stories = Story.objects.filter(is_public=True).order_by('-created_on')
    return render(request, 'stories/story_list.html', {'stories': stories})

def story_detail(request, story_id):
    story = get_object_or_404(Story, id=story_id, is_public=True)
    chapters = story.chapters.all().order_by('created_on')
    return render(request, 'stories/story_detail.html', {
        'story': story,
        'chapters': chapters
    })

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