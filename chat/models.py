from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Chat(models.Model):
    title=models.CharField(max_length=15,default='New chat')
    subtitle=models.TextField(default="Start a new convesation")
    created_at=models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,default=None)
    
    
    
class Message(models.Model):
    chat=models.ForeignKey(Chat,on_delete=models.CASCADE)
    message = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

