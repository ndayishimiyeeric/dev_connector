from django.db import models
from users.models import Profile
import uuid


# Create your models here.

class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    owner = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    project_image = models.ImageField(null=True, blank=True, default="defaultProject.jpg")
    source_code = models.URLField(null=True, blank=True, max_length=2000)
    live_preview = models.URLField(null=True, blank=True, max_length=2000)
    votes_count = models.IntegerField(default=0, blank=True, null=True)
    votes_ratio = models.IntegerField(default=0, blank=True, null=True)
    tags = models.ManyToManyField('Tag', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['created_at']

    @property
    def save_votes(self):
        reviews = self.review_set.all()
        voteCount = reviews.count()
        upVoteCount = reviews.filter(value='up').count()

        if voteCount > 0:
            votes_ratio = (upVoteCount / voteCount) * 100
        else:
            votes_ratio = 0

        self.votes_count = voteCount
        self.votes_ratio = votes_ratio
        self.save()

    @property
    def getReviewers(self):
        reviewers = self.review_set.all().values_list('owner__id', flat=True)
        return reviewers


class Review(models.Model):
    REVIEW_CHOICES = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote'),
    )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True, max_length=200)
    value = models.CharField(choices=REVIEW_CHOICES, max_length=10)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [['owner', 'project']]

    def __str__(self):
        return self.value


class Tag(models.Model):
    name = models.CharField(max_length=100)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
