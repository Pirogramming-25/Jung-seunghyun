from django.db import models

# Create your models here.
class DevTool(models.Model):
    name = models.CharField(max_length=100)
    kind = models.CharField(max_length=100)
    content = models.TextField()
    
    def __str__(self):
        return self.name

class Idea(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='ideas/')
    content = models.TextField()
    interest = models.IntegerField(default=0)
    devtool = models.ForeignKey(DevTool, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class IdeaStar(models.Model):
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=40)