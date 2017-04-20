from django import forms
from .models import *

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget = forms.PasswordInput)


class UserRegisterForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)

    def check_username(self):
        username = self.cleaned_data.get('username')
        q1 = users.objects(username__exists = username).scalar()
        if not q1:
            raise forms.ValidationError("This username is already taken")
        return username




