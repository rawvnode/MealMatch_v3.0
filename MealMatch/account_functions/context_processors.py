from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required

def include_login_form(request):
    form = UserLoginForm(request.POST or None)
    return {'loginForm': form}


def get_user(request):
    try:
        mongouser = Profile.objects.get(user_id_reference = request.user.id)
    except:
        mongouser = None
    return{'user': request.user, 'mongouser': mongouser}


def breadcrumb(request):

    string = request.path[0:-request.path.rfind("/")] #takes away the last part of the url, which instead should be handled by the respective view function

    print("string: ", string)
    array = []
    temp_array = string.split("/")
    for element in temp_array:
        if element != "":
            array.append(element)
            print("hallå " ,element)



    return {"base": string, "array": array}



