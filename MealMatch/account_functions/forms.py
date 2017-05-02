from django import forms
from .models import *
from mongoengine.django.auth import *
from django.contrib.auth import authenticate, login, logout

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget = forms.PasswordInput)


    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        user = authenticate(username = username, password = password)
        if username and password:
            if not user:
                raise forms.ValidationError("Wrong user or password")
            if not user.check_password(password):
                raise forms.ValidationError("Wrong user or password")
        return super(UserLoginForm, self).clean()



class UserRegisterForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(widget = forms.PasswordInput, required = True)
    mail = forms.CharField(required=True)


    def check_username(self):
        username = self.cleaned_data.get('username')
        try:
            q1 = User.objects.get(username=username)
            raise forms.ValidationError("This username is already taken")
        except DoesNotExist: #if no users in the database exist with that particular username
            print("test")
            return username

class AddRecipeForm(forms.Form):
    title = forms.CharField()
    #preperation_time = forms.CharField()
    #servings = forms.CharField()
    #directions = forms.CharField()
    #ingredients = forms.CharField()
    #amount = forms.CharField()
    #unit = forms.ChoiceField(choices=[(x, x) for x in range(1, 32)])
    #category = forms.CharField()
    #picture_url = forms.URLField()
#




