from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # username, password, email 등은 AbstractUser가 이미 제공
    profile_image = models.ImageField(
        upload_to='profiles/', blank=True, null=True
    )
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.username

class Follow(models.Model):
    # from_user = 팔로우 하는 사람(나), to_user = 상대
    from_user = models.ForeignKey(
        'accounts.User',
        on_delete = models.CASCADE,
        related_name = 'following'
    )
    to_user = models.ForeignKey(
        'accounts.User',
        on_delete = models.CASCADE,
        related_name = 'followers'
    )
    class Meta:
        unique_together = ('from_user', 'to_user') # 같은 사람 중복 팔로우 방지
        
    def __str__(self):
        return f'{self.from_user.username} → {self.to_user.username}'