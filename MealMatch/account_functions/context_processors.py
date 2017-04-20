from .forms import *

def include_login_form(request):
    from django.contrib.auth.forms import AuthenticationForm
    form = UserLoginForm(request.POST or None)
    #form = "test"
    return {'form': form}