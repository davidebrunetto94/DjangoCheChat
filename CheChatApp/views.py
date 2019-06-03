from django.shortcuts import render
from django.shortcuts import render

from CheChatApp.models import User


def user_listing(request):
    """View with the list of users"""
    return render(request, 'users/user_listing.html', {'users': User.objects.all()})
