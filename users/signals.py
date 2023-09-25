from django.db.models.signals import post_save, post_delete

from users.models import UserAccount
from .models import Profile


def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name
        )


def updateUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user

    if not created:
        user.username = profile.username
        user.email = profile.email
        user.first_name = profile.first_name
        user.last_name = profile.last_name
        user.save()


def deleteUser(sender, instance, **kwargs):
    user = instance.user
    user.delete()


post_save.connect(createProfile, sender=UserAccount)
post_save.connect(updateUser, sender=Profile)
post_delete.connect(deleteUser, sender=Profile)
