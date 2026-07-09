from django.db import models
from django.conf import settings


class Story(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='stories'
    )
    created_at = models.DateTimeField(auto_now_add=True)   # 24시간 판단에 사용
    
    def __str__(self):
        return f'{self.author.username}의 스토리 ({self.id})'



class StoryImage(models.Model):
    story = models.ForeignKey(
        Story, on_delete=models.CASCADE, related_name='images'
    )
    image = models.ImageField(upload_to='stories/')
    
    def __str__(self):
        return f'{self.story.author.username}의 스토리 사진 ({self.id})'