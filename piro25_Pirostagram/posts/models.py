from django.db import models
from django.conf import settings


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts',
    )
    caption = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']   # 최신 글이 위로

    def __str__(self):
        return f'{self.author.username}의 게시글 ({self.id})'


class PostImage(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='images'
    )
    image = models.ImageField(upload_to='posts/')

class Like(models.Model):
    # user = 좋아요를 누른 사람
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='likes',
    )
    # post = 좋아요가 눌린 게시글
    # Post에서 Like로 역방향 조회(related_name = 역방향 조회 이름을 정하는 옵션)
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE, #연결된 객체가 삭제되면 이 객체도 같이 삭제됨
        related_name='likes',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # 같은 사람이 같은 글에 좋아요를 두 번 못 누르게 막음
        unique_together = ('user', 'post')