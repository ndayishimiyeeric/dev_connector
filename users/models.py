import uuid
from itertools import chain

from django.apps import apps
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)
        email = email.lower()

        user = self.model(
            email=email,
            **kwargs
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **kwargs):
        user = self.create_user(
            email,
            password=password,
            **kwargs
        )

        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


def generate_unique_username(email):
    email_prefix = email.split('@')[0]

    base_username = email_prefix[:45]
    username = base_username
    counter = 1

    while UserAccount.objects.filter(username=username).exists():
        username = f"{base_username}{counter}"
        counter += 1

    return username


class UserAccount(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, max_length=255)

    username = models.CharField(max_length=50, unique=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = generate_unique_username(self.email)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email


class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
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
    following = models.ManyToManyField("self", through="Follower", symmetrical=False, related_name="followers",
                                       blank=True)
    is_online = models.BooleanField(default=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user.username)

    def feed_items(self):
        Project = apps.get_model('projects', 'Project')
        Review = apps.get_model('projects', 'Review')

        following_profiles = self.following.all()

        project_feed = Project.objects.filter(owner__in=following_profiles)
        follow_feed = Follower.objects.filter(sender_profile__in=following_profiles)
        review_feed = Review.objects.filter(owner__in=following_profiles)
        education_feed = Education.objects.filter(owner__in=following_profiles)
        experience_feed = Experience.objects.filter(owner__in=following_profiles)
        skill_feed = Skill.objects.filter(owner__in=following_profiles)

        for project in project_feed:
            if project.created_at == project.updated_at:
                project.object_type = 'ProjectCreated'
            else:
                project.object_type = 'ProjectUpdated'

        for follow in follow_feed:
            follow.object_type = 'Follower'

        for review in review_feed:
            review.object_type = 'Review'

        for education in education_feed:
            education.object_type = 'Education'

        for experience in experience_feed:
            experience.object_type = 'Experience'

        for skill in skill_feed:
            skill.object_type = 'Skill'

        combined_feed = sorted(
            chain(project_feed, follow_feed, review_feed, education_feed, experience_feed, skill_feed),
            key=lambda instance: instance.created_at, reverse=True)
        return combined_feed


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
        if self.is_current:
            self.to_date = None
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
        if self.is_current:
            self.to_date = None
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


class Follower(models.Model):
    sender_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True,
                                       related_name='sent_follows')
    receiver_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True,
                                         related_name='received_follows')
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return self.sender_profile.user.username + ' started following ' + self.receiver_profile.user.username

    class Meta:
        unique_together = [['sender_profile', 'receiver_profile']]

    @property
    def get_followers(self):
        # a flat list of id of all followers
        return self.sender_profile.followers.values_list('sender_profile__id', flat=True)

    @property
    def get_following(self):
        # a flat list of id of all following
        return self.sender_profile.following.values_list('receiver_profile__id', flat=True)


class News(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
