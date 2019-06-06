from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class ChatUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profileImage = models.URLField('Profile image URL', default='')
    lastAccess = models.DateTimeField('Last access', default=timezone.now)


class Chat(models.Model):
    title = models.CharField('Title', max_length=30)
    # se non è un gruppo, title = None
    participants = models.ManyToManyField(User, blank=True, default=None)


class PhoneBook(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='+', primary_key=True)
    contacts = models.ManyToManyField(User)


class Message(models.Model):
    text = models.CharField('Text', max_length=5000)
    timestamp = models.DateTimeField('Timestamp')
    sender = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
