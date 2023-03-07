from django.db import models
import datetime
from users.models import Profile
import uuid
from authentication.models import User

# Create your models here.

class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    owner = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    project_image = models.ImageField(null=True, blank=True, default="defaultProject.jpg" )
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


    votes_count = models.IntegerField(default=0, blank=True, null=True)
    votes_ratio = models.IntegerField(default=0, blank=True, null=True)
    tags = models.ManyToManyField('Tag', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Review(models.Model):
    REVIEW_CHOICES = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote'),
    )
    # user
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True, max_length=200)
    value = models.CharField(choices=REVIEW_CHOICES, max_length=10)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.value
    

class Tag(models.Model):
    name = models.CharField(max_length=100)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name