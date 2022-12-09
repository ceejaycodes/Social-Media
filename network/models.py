from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone



class User(AbstractUser):
    avatar_url = models.URLField(blank=True, null=True)
    following = models.ManyToManyField("self",related_name='userfollowing', blank=True, null=True, symmetrical=False)
    followers = models.ManyToManyField("self",related_name='userfollowers', blank=True, null=True, symmetrical=False)
    bio = models.TextField(blank=True, null=True)
    
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.username,
            }
    

    
    


class Post(models.Model):
    post = models.TextField(blank=True, verbose_name="")
    author = models.ForeignKey(User, on_delete=models.CASCADE,related_name='authors')
    time = models.DateTimeField(default=timezone.now)
    liked_by = models.ManyToManyField(User, related_name='likers', blank=True)
    def __str__(self):
        return f"{self.post} by {self.author}"
    
    def serialize(self):
        return {
            "id": self.id,
            "author": self.author,
            "post": self.post,
            "likes": [likers.name for likers in self.liked_by.all()],
            "time": self.time.strftime("%b %d %Y, %I:%M %p")
            }
    
    