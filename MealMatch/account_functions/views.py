from django.shortcuts import render
from django.http import HttpResponse
from mongoengine.django.auth import *
from django.contrib.auth import authenticate, login, logout
from account_functions.models import *
from django.contrib.auth.decorators import login_required
from mongoengine import *
from .forms import *

@login_required(redirect_field_name = "account_functions/login.html")
def delete_field(request):
    if request.method == "POST":
        users.objects(username= request.POST['your_name']).delete()
        return render(request, "account_functions/delete_field.html")
    else:
        return render(request, "account_functions/delete_field.html")


@login_required(redirect_field_name = "account_functions/login.html")
def update_table(request):   #change profile settings
    if request.method == "POST":
        users.objects(username =  request.POST['old_name']).update(set__username = request.POST['new_name'])
        return HttpResponse("You renamed your account to:",request.POST['new_name'] )
    else:
        return render(request,"account_functions/update_table.html")


def register_view(request):
    title = "Register"
    form = UserRegisterForm(request.POST or None)
    context = {
        "form": form,
        "title": title
    }
    if form.is_valid():
        mail = form.cleaned_data.get('mail')
        password = form.cleaned_data.get('password')
        username = form.check_username()
        user = users(username = username, password = password, mail = mail)
        user.save()



    return render(request, "account_functions/create_user.html", context)




def login_view(request):
    form = UserLoginForm(request.POST or None)
    title = "Login"
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        def clean(self, *args, **kwargs):
            pass
    return render(request, "account_functions/login.html", {"form": form, "title" : title})



@login_required(redirect_field_name = "account_functions/login.html")
def user_logout(request):
    logout(request)
    return render(request, "account_functions/login.html")

@login_required(redirect_field_name = "account_functions/login.html")
def upload_recipes(request):
    # ladda upp ett recept till databasen
    return

@login_required(redirect_field_name = "account_functions/login.html")
def admin_page(request):
    # funktioner till admin
    return

@login_required(redirect_field_name = "account_functions/login.html")
def user_page(request):
    # funktioner till vanlig användare
    return

