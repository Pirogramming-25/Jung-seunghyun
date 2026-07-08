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