from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required

def include_login_form(request):
    from django.contrib.auth.forms import AuthenticationForm
    form = UserLoginForm(request.POST or None)
    #form = "test"
    return {'loginForm': form}


def is_logged_in(request):
    #import ipdb;
    #ipdb.set_trace()

    #try:
       # mongouser = Profile.objects.filter()
    return{'user': request.user}


