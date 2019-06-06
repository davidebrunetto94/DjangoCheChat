from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.shortcuts import render, redirect
from CheChatApp.models import Chat, PhoneBook, ChatUser
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth import get_user_model



def user_listing(request):
    """View with the list of users"""
    return render(request, 'users/user_listing.html', {'users': User.objects.all()})


def get_user_info(request, user_id):
    """Get user info"""

    user = User.objects.filter(id=user_id).values_list('username', 'last_login')
    chatUser = ChatUser.objects.filter(user_id=user_id).values_list('profileImage', flat=True)

    if user.exists():

        if(chatUser.exists()):
            thumbnail = list(chatUser)[0]
        else:
            thumbnail = ''

        response = {
            'username': list(user)[0][0],
            'thumbnail': thumbnail,
            'lastlogin': list(user)[0][1].strftime('%d %b %Y')
        }
    else:
        response = {
            'state': 'user not found'
        }

    return JsonResponse(response)

def get_id_from_username(request, username):
    """Get id by username"""
    user = User.objects.filter(username=username).values_list('id', flat=True)

    if user.exists():
        response = {'state': 'successful', 'id': list(user)[0]}
    else:
        response = {'state': 'username not found'}

    return JsonResponse(response)


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
            'id': chat.id,
            'owner_id': chat.participants.values_list()[0][0]
        }
    else:
        response = {
            'state': 'no auth'
        }

    return JsonResponse(response)


def add_participant(request, user_id, chat_id):
    """
        Add a participant to a chat
        Only participants of a chat can add other
        An user can add himself, only if the chat doesn't have any participants (so it's the creator)
    """

    # TODO: controllare gli il participiant sia amico dell'utente che aggiunge

    if is_participants(chat_id, request.user.id) or \
            (request.user.id == int(user_id) and len(Chat.objects.get(id=chat_id).participants.values_list()) == 0):

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


def get_contacts(request):
    phonebook = PhoneBook.objects.filter(owner=request.user)

    response = {
        'state': 'successful',
        'contacts': list(phonebook.values_list('contacts', flat=True))
    }

    return JsonResponse(response)


def add_contact(request, added_user_id):
    if not PhoneBook.objects.filter(owner=request.user).exists():
        PhoneBook(owner=request.user).save()

    phonebook = PhoneBook.objects.get(owner=request.user)

    if not User.objects.filter(id=added_user_id).exists():
        response = {'state': 'user not found'}
    elif phonebook.contacts.filter(id=added_user_id).exists():
        response = {'state': 'already friend'}
    else:
        phonebook.contacts.add(User.objects.get(id=added_user_id))
        response = {'state': 'successful'}

    return JsonResponse(response)


def is_participants(chat_id, user_id):
    """Check if the user is a participant of the chat"""

    chat = Chat.objects.get(id=chat_id)

    for participant in chat.participants.values_list():
        if participant[0] == user_id:
            return True

    return False


def change_chat_title(request, user_id, chat_id, new_chat_title):
    chat = Chat.objects.get(id=chat_id)
    chat_owner_id = chat.participants.values_list()[0][0]
    print(chat)
    if (chat_owner_id == request.user.id):
        #This means the user is the one who created the chat

        Chat.objects.get(id=chat_id).Title = new_chat_title
        print("if")
        response = {
            'state': 'successful',
        }

    else:
        response = {
            'state': 'unsuccessful',
        }
        print("Not the owner")

    return JsonResponse(response)
