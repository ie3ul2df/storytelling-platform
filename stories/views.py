from django.shortcuts import render
from .models import Story

def story_list(request):
    stories = Story.objects.filter(is_public=True).order_by('-created_on')
    return render(request, 'stories/story_list.html', {'stories': stories})
