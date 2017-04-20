from .forms import *

def include_login_form(request):
    from django.contrib.auth.forms import AuthenticationForm
    form = UserLoginForm(request.POST or None)
    #form = "test"
    return {'form': form}

def is_loggeed_in(request):
    isloggedin = False
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        isloggedin = True
    return{'isloggedín': isloggedin}