from django import forms
from .models import *
from mongoengine.django.auth import *
from django.contrib.auth import authenticate, login, logout

class CommentForm(forms.Form):
    comment =  forms.CharField(widget = forms.Textarea, label="")
    comment2 = forms.TextInput()

