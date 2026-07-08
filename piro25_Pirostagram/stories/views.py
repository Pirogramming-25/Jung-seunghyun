from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Story, StoryImage


@login_required
def story_create(request):
    if request.method == 'POST':
        images = request.FILES.getlist('images')   # 여러 장 받기
        if images:
            story = Story.objects.create(author=request.user)
            for img in images:
                StoryImage.objects.create(story=story, image=img)
    return redirect('posts:feed')