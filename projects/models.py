from django.db import models
import uuid

# Create your models here.

class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    source_code = models.URLField(null=True, blank=True, max_length=2000)
    live_preview = models.URLField(null=True, blank=True, max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
