from django.urls import path
from .views import *
from .views import del_chat

urlpatterns = [
    path("",main_app,name="main_chat"),
    path("get_chats/",get_chats,name="get_chats"),
    path("delete_chat/<int:id>",del_chat,name="delete_chat"),
    path("send/",send_prompt,name="send_prompt"),
    path("new_chat/",new_chat,name="new_chat"),
    path("load_chat/<int:id>",load_chat,name="load_chat"),
    path("login/",login_page,name="login"),
    path("logout/",logout_user,name="logout"),
    path('register/',register_user,name='register'),
]