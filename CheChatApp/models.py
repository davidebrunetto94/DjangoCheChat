from django.db import models

class User(models.Model):
    """User model"""
    username = models.CharField('Username', max_length=20)
    password = models.CharField('Password', max_length=100)
    fullname = models.CharField('Full name', max_length=100)
    email = models.EmailField('Email')
    profileImage = models.URLField('Profile image URL')
    lastAccess = models.DateTimeField('Last access')


class Chat(models.Model):
    title = models.CharField('Title', max_length=30)
    # se non è un gruppo, title = None
    participants = models.ManyToManyField(User)

class PhoneBook(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='+', primary_key=True)
    contacts = models.ManyToManyField(User)

class Message(models.Model):
    text = models.CharField('Text', max_length=5000)
    timestamp = models.DateTimeField('Timestamp')
    sender = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)


