from django.shortcuts import render, redirect
from django.http import HttpResponse
from mongoengine.django.auth import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from mongoengine import *
from .forms import *
from django.http import HttpResponseRedirect

# @login_required(redirect_field_name = "account_functions/login.html")
# def delete_field(request):
#     if request.method == "POST":
#         users.objects(username= request.POST['your_name']).delete()
#         return render(request, "account_functions/delete_field.html")
#     else:
#         return render(request, "account_functions/delete_field.html")
#
#
# @login_required(redirect_field_name = "account_functions/login.html")
# def update_table(request):   #change profile settings
#     if request.method == "POST":
#         users.objects(username =  request.POST['old_name']).update(set__username = request.POST['new_name'])
#         return HttpResponse("You renamed your account to:",request.POST['new_name'] )
#     else:
#         return render(request,"account_functions/update_table.html")


@login_required
def my_pantry(request):

    user_id = request.user.id
    user_profile = Profile.objects.get(user_id_reference = user_id)
    my_pantry = user_profile.Pantry
    return render(request,"account_functions/my_pantry.html", {"pantry": my_pantry})



def login_view(request):


    next = request.GET.get('next')
    title = "Login"
    form = UserLoginForm(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username = username, password = password)
        #user.backend = 'mongoengine.django.auth.MongoEngineBackend'
        #print("login")
        login(request, user)
        #if next:
            #return redirect(next)
        return redirect("/")
        #request.session.set_expiry(60 * 60 * 1)
        #print(request.user.is_authenticated())

    return render("startpage.html", {"form": form, "title" : title})

def register_view(request):
    next = request.GET.get('next')
    title = "Register"
    form = UserRegisterForm(request.POST or None)

    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        #username = form.check_username()
        #user = User.create_user(username = username, password = password)
        #mail = form.cleaned_data.get('mail')

        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        #if next:
         #   return redirect(next)
        return redirect("/")

    context = {
        "form": form,
        "title": title
    }

    return render(request, "account_functions/create_user.html", context)




def logout_view(request):
    logout(request)
    return redirect("/")


# @login_required(redirect_field_name = "account_functions/login.html")
# def user_logout(request):
#     logout(request)
#     print("logged out?")
#     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
#
# @login_required(redirect_field_name = "account_functions/login.html")
# def upload_recipes(request):
#     # ladda upp ett recept till databasen
#     return
#
# @login_required(redirect_field_name = "account_functions/login.html")
# def admin_page(request):
#     # funktioner till admin
#     return
#
# @login_required(redirect_field_name = "account_functions/login.html")
# def user_page(request):
#     # funktioner till vanlig användare
#     return

