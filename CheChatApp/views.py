import datetime

from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from CheChatApp.models import Chat, PhoneBook, ChatUser, Message
from django.contrib.auth.models import User
from django.http import JsonResponse


def user_listing(request):
    """View with the list of users"""
    list_username = []
    list_id = []
    for user in User.objects.all():
        list_username.append(user.username)
        list_id.append(user.id)

    response = {
        'user': list_username,
        'id': list_id
    }
    return JsonResponse(response)


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
            'lastlogin': '' if list(user)[0][1] is None else list(user)[0][1].strftime('%d %b %Y')
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


def get_current_user_id(request):
    response = {
        'state': 'successful',
        'id': request.user.id
    }

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

   #tested
def info_chat_by_id(request, chat_id):
    chat = Chat.objects.filter(id=chat_id)

    if len(chat[0].participants.all().values_list()) > 2:
        group = "true"
    else:
        group = "false"

    response = {
        'title': chat[0].title,
        'isGroup': group,
        'lastMessage': chat[0].lastMessage
    }

    return JsonResponse(response)

    #tested
def get_chat_by_user(request):
    """Get chat of the user"""

    chat = Chat.objects.filter(participants__in=str(request.user.id)).order_by('-lastMessage')
    response = {}
    
    if chat.exists():
        response = {
            'state': 'successful',
            'chat': list(chat.values("id"))
        }
    else:
        response = {
            'state': 'chat doesn\'t exist'
        }

    return JsonResponse(response)


def get_last_message(request, chat_id):
    """Get the last message of the user"""
    chat = Chat.objects.filter(id=chat_id)

    if chat.exists() and is_participants(chat_id, request.user.id):
        message = list(Message.objects.filter(chat=chat_id).order_by('-timestamp').values("text", "timestamp"))

        if len(message) > 0:
            response = {
                'state': 'successful',
                'message': message[0]
            }
        else:
            response = {
                'state': 'successful',
                'message': []
            }

    elif not is_participants(chat_id, request.user.id):
        response = {
            'state': 'not a participant'
        }
    else:
        response = {
            'state': 'chat not found'
        }

    return JsonResponse(response)


    #tested
def new_chat(request, title=""):
    """Create a new"""
    # TODO: controllare se l'utente è amico
    if request.user.is_authenticated:
        chat = Chat.objects.create(title=title)
        chat.save()

        add_participant(request, request.user.id, chat.id)

        if title == "":
            chat.title = "Chat"
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


def is_friend(current_user_id, user_id):
    if current_user_id == int(user_id):
        return True

    pb = PhoneBook.objects.get(owner=User.objects.get(id=current_user_id))
    return pb.contacts.filter(id=user_id).exists()


def add_participant(request, user_id, chat_id):
    """
        Add a participant to a chat
        Only participants of a chat can add other
        An user can add himself, only if the chat doesn't have any participants (so it's the creator)
    """

    # TODO: aggiungere un titolo alla chat se da 2 persone si passa a 3 (va bene anche il nome del creatore)
    if is_friend(request.user.id, user_id):
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
    else:
        response = {
            'state': 'user is not friend'
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

    #tested
def get_contacts(request):
    if not PhoneBook.objects.filter(owner=request.user).exists():
        PhoneBook(owner=request.user).save()
    #try:
    #    phonebook = PhoneBook.objects.get(owner=request.user)
    #except PhoneBook.DoesNotExist:
    #    phonebook = None
    #    response = {'state': 'phonebook not found'}

    phonebook = PhoneBook.objects.get(owner=request.user)
    response = {
        'state': 'successful',
        'contacts': list(phonebook.contacts.values_list(flat=True))
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

    #tested
def delete_contact(request, user_to_delete_id):
    try:
        phonebook = PhoneBook.objects.get(owner=request.user)
    except PhoneBook.DoesNotExist:
        phonebook = None
        response = {'state': 'phonebook not found'}

    if User.objects.filter(id=user_to_delete_id).exists() and phonebook is not None \
            and phonebook.contacts.filter(id=user_to_delete_id).exists():
        response = {'state': 'successful'}
        phonebook.contacts.get(id=user_to_delete_id).delete()
    elif phonebook is not None and not phonebook.contacts.filter(id=user_to_delete_id).exists():
        response = {'state': 'user does not exist'}

    return JsonResponse(response)


@csrf_exempt
def send_message(request):
    chat_id = request.POST.get('id')

    chat = Chat.objects.filter(id=chat_id)

    if chat.exists() and is_participants(chat_id, request.user.id):
        message = Message(text=request.POST.get('message_body'),
                sender=list(User.objects.filter(id=request.user.id))[0],
                chat=list(Chat.objects.filter(id=chat_id))[0])
        message.save()

        chatSave = Chat.objects.get(id=chat_id)
        chatSave.lastMessage = datetime.datetime.now()
        chatSave.save()

        print(datetime.datetime.now())

        response = {'state': 'successful', 'message_id' : message.id}
    else:
        response = {'state': 'chat does not exist'}

    return JsonResponse(response)


def get_messages_by_id(request, chat_id):
    chat = Chat.objects.filter(id=chat_id)
    if chat.exists() and is_participants(chat_id, request.user.id):
        messages = Message.objects.filter(chat=chat_id).order_by('timestamp')
        response = {
            'state': 'successful',
            'messages': list(messages.values('sender', 'text', 'timestamp'))
        }
    else:
        response = {'state': 'chat does not exist'}

    return JsonResponse(response)

    #tested
def is_participants(chat_id, user_id):
    """Check if the user is a participant of the chat"""

    chat = Chat.objects.get(id=chat_id)
    return chat.participants.filter(id=user_id).exists()


def exit_group(request, chat_id):
    if is_participants(chat_id, request.user.id):
        chat = Chat.objects.get(id=chat_id)
        chat.participants.remove(request.user.id)
        response = {'state': 'successful'}
    else:
        response = {'state': 'fail'}

    return JsonResponse(response)


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
