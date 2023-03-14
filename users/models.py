from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
import uuid
from django.db.models.signals import post_save, post_delete


# Create your models here.

class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    username = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=600, null=True, blank=True)
    headline = models.CharField(max_length=200, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    profile_image = models.ImageField(null=True, blank=True, upload_to='profiles/', default='profiles/defaultUser.png')
    location = models.CharField(max_length=200, null=True, blank=True)
    linkedin = models.CharField(max_length=200, null=True, blank=True)
    github = models.CharField(max_length=200, null=True, blank=True)
    website = models.CharField(max_length=200, null=True, blank=True)
    twitter = models.CharField(max_length=200, null=True, blank=True)
    youtube = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user.username)


class Skill(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return self.name


class Experience(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    company = models.CharField(max_length=200, null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    from_date = models.DateField(null=True, blank=True)
    to_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    def clean(self):
        if (self.is_current and self.to_date is not None) or self.from_date is None or (
                self.to_date is None and not self.is_current) or (self.to_date == self.from_date):
            raise ValidationError('Invalid date range, please check your dates.')
        if self.to_date is not None and (self.to_date < self.from_date and self.to_date < timezone.now().date()):
            raise ValidationError(
                'Invalid date range, please check your dates. got to_date: {} and from_date: {}'.format(self.to_date,
                                                                                                        self.from_date))

    def save(self, *args, **kwargs):
        self.clean()
        super(Experience, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Education(models.Model):
    DEGREE_CHOICES = (
        ('certificate', 'Certificate'),
        ('diploma', 'Diploma'),
        ('associate', 'Associate'),
        ('bachelor', 'Bachelor'),
        ('master', 'Master'),
        ('doctorate', 'Doctoral'),
    )

    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    school = models.CharField(max_length=200, null=True, blank=True)
    degree = models.CharField(choices=DEGREE_CHOICES, max_length=100, null=True, blank=True)
    field_of_study = models.CharField(max_length=200, null=True, blank=True)
    from_date = models.DateField(null=True, blank=True)
    to_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    def clean(self):
        if (self.is_current and self.to_date is not None) or self.from_date is None or (
                self.to_date is None and not self.is_current) or (self.to_date == self.from_date):
            raise ValidationError('Invalid date range, please check your dates.')
        if self.to_date is not None and (self.to_date < self.from_date and self.to_date < timezone.now().date()):
            raise ValidationError(
                'Invalid date range, please check your dates. got to_date: {} and from_date: {}'.format(self.to_date,
                                                                                                        self.from_date))

    def save(self, *args, **kwargs):
        self.clean()
        super(Education, self).save(*args, **kwargs)

    def __str__(self):
        return self.school
