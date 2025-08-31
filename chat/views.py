from django.shortcuts import render,redirect,HttpResponse
from django.http import JsonResponse,StreamingHttpResponse
import ollama
from .models import Chat,Message,User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
import asyncio

# Create your views here.


def login_page(request):
    if request.user.is_authenticated:
        return redirect("main_chat")
    context={"theme":"dark"}
    if request.method=="POST":
        username=request.POST["username"]
        pswrd=request.POST["password"]
  
        user=authenticate(request=request,username=username,password=pswrd)
        if user is not None:
            login(request,user=user)
            return redirect("main_chat")            
        else:
            messages.error(request,"username does not exist or Wrong password")
            
    
    return render(request,"reg_login.html",context)


def logout_user(request):
    lg=logout(request=request)
    return redirect("login")

def register_user(request):
    if request.user.is_authenticated:
        return redirect("main_chat")
    
    return render(request,"register.html",{"theme":"dark"})

async def generate_chat_title(chat,rsp,msg):
    if chat.title=="New chat":
        title=''
        chat.subtitle=msg
        for i in ollama.chat(model='qwen2.5-coder:latest', messages=[{'role': 'user','content':f"genera un titulo lo mas corto posible sobre el siguiente prompt: {msg}. el cual obtuvo una respuesta por parte de la ia de: {rsp}. la respuesta no debe de tener mas de 7 palabras"}],stream=True):
            title+=i.message["content"]
        chat.title=title
        chat.save()

@login_required(login_url="login")
def del_chat(request,id):
    Chat.delete(Chat.objects.get(id=id))
    
    return redirect("main_chat")


@login_required(login_url="login")
def main_app(request):
    models=["qwen2.5-coder:latest","qwen-2"]
    return render(request,"chat.html",{"theme":"dark",
                                       "models":models})

@login_required(login_url="login")
def send_prompt(request):
    models=ollama.list()
    msg=''
    id_chat=request.POST["Chat_ID"]
    chat=Chat.objects.get(id=id_chat)
    if chat==None:
        messages.error("You must create a chat first")
        return redirect("main_chat")
        #return JsonResponse({"succeded":"no","error":"chat not found"})
    for i in ollama.chat(model='qwen2.5-coder:latest', messages=[{'role': 'user','content': request.POST["prompt"]}],stream=True):
        msg+=i.message["content"]
    Message(message=request.POST["prompt"],response=msg,chat=chat).save()
    #asyncio.run( generate_chat_title(chat,msg,request.POST["prompt"]))
    return JsonResponse({"succeded":"yes","response":msg})


@login_required(login_url="login")
def new_chat(request):
    new_chat=Chat(user=request.user).save()
    return JsonResponse({"succeded":"yes","chat":new_chat,"time":new_chat.created_at})

@login_required(login_url="login")
def get_chats(request):
    chats=Chat.objects.filter(user=request.user)
    for chat in chats:
        chat.created_humanized=chat.created_at.strftime('%B %D  , %Y')
    chats=list(chats.values())
    if len(chats)>0:
        return JsonResponse({"succeded":"yes","chats":chats})
    else:
        return JsonResponse({"succeded":"no"})

@login_required(login_url="login")
def load_chat(request,id):
    messages=list(Message.objects.filter(chat=Chat.objects.get(id=id)).values())
    if len(messages)>0:
        return JsonResponse({"succeded":"yes","messages":messages})
    else:
        return JsonResponse({"succeded":"no"})
    