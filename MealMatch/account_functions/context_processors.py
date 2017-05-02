from .forms import *
from django.contrib.auth.decorators import login_required

def include_login_form(request):
    from django.contrib.auth.forms import AuthenticationForm
    form = UserLoginForm(request.POST or None)
    #form = "test"
    return {'loginForm': form}


def is_logged_in(request):
    #import ipdb;
    #ipdb.set_trace()

    print("cookie ", request.user)

    return{'user': request.user}
