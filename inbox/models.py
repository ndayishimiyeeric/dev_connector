from django.db import models

from users.models import Profile


# Create your models here.


class Conversation(models.Model):
    participants = models.ManyToManyField(Profile, related_name='conversations')
    subject = models.CharField(max_length=200)
    starred = models.ManyToManyField(Profile, related_name='starred_conversations', blank=True)
    unread = models.ManyToManyField(Profile, related_name='unread_conversations', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sent_messages')
    body = models.TextField()
    started_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.body[:50]


class Reply(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='replies')
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sent_replies')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.body[:50]
