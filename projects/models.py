from django.db import models
import datetime
import uuid
from authentication.models import User

# Create your models here.

class Project(models.Model):
    title = models.CharField(max_length=200,null=True)
    description = models.TextField(blank=True)
    source_code = models.URLField(null=True, blank=True, max_length=2000)
    live_preview = models.URLField(null=True, blank=True, max_length=2000)
    image=models.ImageField(upload_to="photos/projects/",null=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="projects")
    created_at = models.DateTimeField(auto_now_add=True)

class Post(models.Model):
    description = models.TextField(blank=True,null=True)
    image=models.ImageField(upload_to="photos/posts/",null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="posts")

    def num_likes(self):
        return self.likes.count()

    def user_has_liked(self, user):
        print("=====================================================")
        #return self.likes.filter(user=user).exists()
    
    def num_comments(self):
        return self.comments.count()

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')


    
