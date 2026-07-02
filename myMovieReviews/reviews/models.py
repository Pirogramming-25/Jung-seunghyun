from django.db import models

# Create your models here.
class Review(models.Model):
        GENRE_CHOICES = [
            ('action', '액션'),
            ('thriller', '스릴러'),
            ('romance', '로맨스'),
            ('comedy', '코미디'),
            ('sf', '공상과학'),
            ('horror', '공포'),
            ('drama', '드라마'),
            ('animaton', '애니메이션'),
        ]
        title = models.CharField(max_length=100)
        release_year = models.IntegerField()
        director = models.CharField(max_length=100)
        actor = models.CharField(max_length=100)
        genre = models.CharField(max_length=50, choices=GENRE_CHOICES)
        rating = models.FloatField()
        running_time = models.IntegerField()
        content = models.TextField()
    
