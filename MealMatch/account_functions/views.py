from django.shortcuts import render
from django.http import HttpResponse
from mongoengine.django.auth import *
from django.contrib.auth import authenticate, login, logout
from account_functions.models import *
from django.contrib.auth.decorators import login_required
from mongoengine import *


@login_required(redirect_field_name = "account_functions/login.html")
def delete_field(request):
    if request.method == "POST":
        users.objects(username= request.POST['your_name']).delete()
        return render(request, "account_functions/delete_field.html")
    else:
        return render(request, "account_functions/delete_field.html")


@login_required(redirect_field_name = "account_functions/login.html")
def update_table(request):
    if request.method == "POST":
        users.objects(username =  request.POST['old_name']).update(set__username = request.POST['new_name'])
        return HttpResponse("You renamed your account to:",request.POST['new_name'] )
    else:
        return render(request,"account_functions/update_table.html")


# Create your views here.
def create_new_user(request):
    if request.method == "POST":
        if users.objects(username = request.POST['mail']) ==  None:

            user = users.create_user(request.POST['mail'], request.POST['pwd'])
            user.save()
            create_staff = False
            if create_staff:
                staff = users(username = "agatonvet", is_staff = True)
                staff.save()
            return HttpResponse('you have created a user')
            #return render(request, "new_user.html")
        else:
            return HttpResponse('username already taken')

    else:

        return render(request, "account_functions/create_user.html")


def login_function(request):
    if request.method == "POST":
        username = request.POST['your_name']
        password = request.POST['pwd']
        user = authenticate(username=username, password=password)

        if user is not None:
            users.backend = 'mongoengine.django.auth.MongoEngineBackend'
            try:
                request.session['user'] = user
                login(request, user)
            except users.DoesNotExist:
                print("error does not exist")
            if user.is_authenticated:
                return render(request, "account_functions/update_table.html")
        else:
            return HttpResponse('login failed')
    else:
        return render(request, "account_functions/login.html")

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

