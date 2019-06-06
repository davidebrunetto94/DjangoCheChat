"""CheChat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from CheChatApp import views
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/logout/', views.logout, name='logout'),
    path('account/contacts/', views.get_contacts),
    path('account/contacts/add/<added_user_id>', views.add_contact),
    path(r'users/', views.user_listing),
    path('users/get/<user_id>', views.get_user_info),
    path('', views.login, name='login'),
    path('chat/new', views.new_chat, name='user_id'),
    path('chat/new/<title>', views.new_chat),
    path('chat/add/participant/<user_id>/<chat_id>', views.add_participant, name='info'),
    path('chat/get/participants/<chat_id>', views.get_participants),
    path('chat/change/title/<user_id>/<chat_id>/<new_chat_title>', views.change_chat_title)
]
