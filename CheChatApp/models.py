from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class ChatUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profileImage = models.URLField('Profile image URL', default='')
    lastAccess = models.DateTimeField('Last access', default=timezone.now)