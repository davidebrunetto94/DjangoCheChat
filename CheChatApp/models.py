from django.db import models


class User(models.Model):
    """User model"""
    username = models.CharField('Username', max_length=20)
    password = models.CharField('Password', max_length=100)
    fullname = models.CharField('Full name', max_length=100)
    email = models.EmailField('Email')
    profileImage = models.URLField('Profile image URL')
    lastAccess = models.DateTimeField('Last access')

