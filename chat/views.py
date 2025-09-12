from django.shortcuts import render,redirect,HttpResponse
from django.http import JsonResponse,StreamingHttpResponse
import ollama
from .models import Chat,Message,User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
import requests
import json


api="http://localhost:11434/api/"

# Create your views here.



#util functions
def get_models():
    url = api+"tags"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        models = [model["model"] for model in data["models"]]
        return models
    else:
        
        return []



#views

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
    if request.method=="POST":
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.save()
            
            login(request,user=user)
            Chat(user=request.user).save()
            return redirect("main_chat")  
        
    form=UserCreationForm
    return render(request,"register.html",{"theme":"dark","form":form})

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
    
    
    models=get_models()
    
    return render(request,"chat.html",{"theme":"dark","models":models})

@login_required(login_url="login")
def send_prompt(request):
    id_chat=request.POST["Chat_ID"]
    chat=Chat.objects.get(id=id_chat)
    if chat==None:
        messages.error("You must create a chat first")
        return JsonResponse({"succeded":"no","error":"chat not found"})

    #this data request to ollama api 
    model_url=api+"generate"
    data_message={
  "model": "qwen2.5-coder:latest",
  "prompt": request.POST["prompt"],
  "stream": False}

    response=requests.post(model_url,json=data_message)
    msg=response.json()["response"] 
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
    