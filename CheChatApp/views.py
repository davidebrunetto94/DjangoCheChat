from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.shortcuts import render, redirect
from CheChatApp.models import Chat
from django.contrib.auth.models import User
from django.http import JsonResponse


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


def new_chat(request, title=""):
    """Create a new"""

    # TODO: controllare se l'utente è amico

    if request.user.is_authenticated:
        chat = Chat.objects.create(title=title)
        chat.save()

        add_participant(request, request.user.id, chat.id)

        response = {
            'state': 'successful',
            'id': chat.id
        }
    else:
        response = {
            'state': 'no auth'
        }

    return JsonResponse(response)


def add_participant(request, user_id, chat_id):
    """Add a participant to a chat"""

    if is_participants(chat_id, request.user.id) or request.user.id == user_id:

        chat = Chat.objects.filter(id=chat_id)

        if chat[0].participants.filter(id=user_id).exists():
            response = {
                'state': 'user exists'
            }
        else:
            chat[0].participants.add(user_id)

            response = {
                'state': 'successful'
            }
    else:
        response = {
            'state': 'not a participant'
        }

    return JsonResponse(response)


def get_participants(request, chat_id):
    """Get participants of a chat"""

    if is_participants(chat_id, request.user.id):
        chat = Chat.objects.get(id=chat_id)

        response = {
            'state': 'successful',
            'participants': list(chat.participants.values('id', 'username'))
        }
    else:
        response = {
            'state': 'not a participant'
        }

    return JsonResponse(response)


def is_participants(chat_id, user_id):
    """Check if the user is a participant of the chat"""

    chat = Chat.objects.get(id=chat_id)

    for participant in chat.participants.values_list():
        if participant[0] == user_id:
            return True

    return False
