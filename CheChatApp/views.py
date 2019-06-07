from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.shortcuts import render, redirect
from CheChatApp.models import Chat, PhoneBook, ChatUser, Message
from django.contrib.auth.models import User
from django.http import JsonResponse


def user_listing(request):
    """View with the list of users"""
    return render(request, 'users/user_listing.html', {'users': User.objects.all()})


def get_user_info(request, user_id):
    """Get user info"""

    user = User.objects.filter(id=user_id).values_list('username', 'last_login')
    chat_user = ChatUser.objects.filter(user_id=user_id).values_list('profileImage', flat=True)

    if user.exists():

        if chat_user.exists():
            thumbnail = list(chat_user)[0]
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


def chat_by_id(request, chat_id):
    """Show selected chat"""

    if request.user.is_authenticated:
        chat = Chat.objects.filter(id=chat_id)
        msg = Message.objects.filter(chat=chat[0])
        list_text = []
        for msgText in msg:
            list_text.append(msgText.text)

        response = {
            'Title Chat': chat[0].title,
            'text': list_text
        }
    else:
        response = {
            'state': 'no auth'
        }

    return JsonResponse(response)


def info_chat_by_id(request, chat_id):

    chat = Chat.objects.filter(id=chat_id)
    i=0
    for p in chat[0].participants.all():
        i = i+1
    if i > 2:
        group = "true"
    else:
        group = "false"

    response = {
        'Title Chat': chat[0].title,
        'Id Char': chat_id,
        'isGroup': group
    }

    return JsonResponse(response)


def lista_chat_by_user(request, user_id):
    user = User.objects.filter(id = user_id)
    lista_chat = Chat.objects.all()
    toreturn = []
    for c in lista_chat:
        for p in c.participants.all():
            if p == user[0]:
                aux = []
                last_message = "no message"
                msg = Message.objects.filter(chat=c)
                for msgText in msg:
                    last_message = msgText.text
                aux.append(c.title)
                aux.append(c.id)
                aux.append(last_message)
                toreturn.append(aux)
    response = {
        'Chat List': toreturn,
    }
    return JsonResponse(response)


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

    return render(request, 'chat.html')


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
    elif request.user.id == int(added_user_id):
        response = {'state': 'you cannot add yourself'}
    else:
        phonebook.contacts.add(User.objects.get(id=added_user_id))
        response = {'state': 'successful'}

    return JsonResponse(response)

def delete_contact(request, user_to_delete_id):
    phonebook = PhoneBook.objects.get(owner=request.user)

    if not User.objects.filter(id=user_to_delete_id).exists() or not phonebook.contacts.filter(id=user_to_delete_id).exists():
        response = {'state' : 'user does not exist'}
    elif phonebook.contacts.filter(id=user_to_delete_id).exists():
        response = {'state' : 'successful'}
        phonebook.contacts.get(id=user_to_delete_id).delete()

    return JsonResponse(response)

# TODO vedere se funziona
def send_message(request, chat_id):
    chat = Chat.objects.filter(id=chat_id)
    if not chat.exists() or not Chat.objects.get(id=chat_id).participants.filter(id=request.id).exists():
        response = {'state' : 'chat does not exist'}
    else:
        Message(text=request.POST.get('message_body'), sender=request.user.id, chat=chat_id).save()
        response = {'state' : 'successful'}
    return JsonResponse(response)


# semmai dovesse servire, altrimenti cancellare
"""def get_chat_messages(request, chat_id):
    chat = Chat.objects.filter(id=chat_id)
    if not chat.exists() or not Chat.objects.get(id=chat_id).participants.filter(id=request.user.id).exists():
        response = {'state' : 'chat does not exist'}
    else:
        messages = Message.objects.filter(chat=chat_id).order_by('-timestamp')
        response = {
            'state' : 'successful',
            'messages' : list(messages.values_list('sender', 'text', 'timestamp'))
        }
    return JsonResponse(response)"""


def is_participants(chat_id, user_id):
    """Check if the user is a participant of the chat"""

    chat = Chat.objects.get(id=chat_id)

    for participant in chat.participants.values_list():
        if participant[0] == user_id:
            return True

    return False


def change_chat_title(request, chat_id, new_chat_title):
    """
    Change the title of a chat
    Only the creator can
    """
    chat = Chat.objects.get(id=chat_id)
    chat_owner_id = chat.participants.values_list()[0][0]

    if chat_owner_id == request.user.id:
        chat = Chat.objects.get(id=chat_id)
        chat.title = new_chat_title
        chat.save()

        response = {
            'state': 'successful',
        }
    else:
        response = {
            'state': 'not the owner',
        }

    return JsonResponse(response)
