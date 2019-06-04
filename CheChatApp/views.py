from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.shortcuts import render, redirect

from django.contrib.auth.models import User


def user_listing(request):
    """View with the list of users"""
    return render(request, 'users/user_listing.html', {'users': User.objects.all()})


def login(request):
    """Login view"""
    if request.method == 'GET':
        # If the user is visiting the login page
        if request.user.is_authenticated:
            return render(request, 'chat.html')
        else:
            return render(request, 'login.html')
    elif request.method == 'POST':
        # If the user done the login
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return render(request, 'chat.html')
        else:
            context = {'error': 'Wrong credentials'}
            return render(request, 'login.html', {'error': context})


def logout(request):
    """Logout views"""
    auth_logout(request)
    return redirect('login')