from django.shortcuts import render, redirect
from django.http import HttpResponse
from mongoengine.django.auth import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from mongoengine import *
from .forms import *
from django.http import HttpResponseRedirect
from recipes.models import recipe
import re


#### pantry function ###
@login_required
def my_pantry(request):

    user_id = request.user.id
    user_profile = Profile.objects.get(user_id_reference = user_id)
    my_pantry = user_profile.Pantry
    return render(request,"account_functions/my_pantry.html", {"pantry": my_pantry})

def editpantry(request):
    input = sanitize_pantry(request.POST.getlist('input[]', ""))
    if (len(input) > 0):
        user_id = request.user.id
        user_profile = Profile.objects.get(user_id_reference=user_id)
        user_profile.Pantry = input
        user_profile.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


### user auth functions ###

def login_view(request):


    title = "Login"
    form = UserLoginForm(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username = username, password = password)

        login(request, user)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def register_view(request):
    next = request.GET.get('next')
    title = "Register"
    form = UserRegisterForm(request.POST or None)

    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()


        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        return redirect("/")

    context = {
        "form": form,
        "title": title
    }

    return render(request, "account_functions/create_user.html", context)



def logout_view(request):
    logout(request)
    print("logged out?")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

### Add recipe functions ####

def handle_bad_input_from_users(bad_string):
    good_string = bad_string.split(":")
    return good_string

def add_recipe(request):
    form = AddRecipeForm(request.POST or None)
    title = 'Add recipe'
    context = {
        "form": form,
        "title": title
    }
    if form.is_valid():
        title_recipe = form.cleaned_data.get('title')
        #preperation_time = form.cleaned_data.get('preperation_time')
        #servings = form.check_username('servings')
        directions_recipe = handle_bad_input_from_users(form.cleaned_data.get('directions'))
        #amount = form.check_username('amount')
        #unit = form.check_username('unit')
        category_recipe = handle_bad_input_from_users(form.cleaned_data.get('category'))
        #picture_url = form.check_username('picture_url')

        recipe_saving=  recipe(title = title_recipe,directions= directions_recipe,category = category_recipe)
        recipe_saving.save()
    return render(request, "account_functions/add_recipe.html", context)


###############HELPER FUNCTIONS################

def sanitize_pantry(list):
    print("#############", list)
    for index in range(len(list)):

        if list[index][-1] == "X":
            list[index] = list[index][:-1]
        list[index] = list[index].replace("\n","")
        list[index] = list[index].replace("  ", "") #RÖR EJ; MAGI

    return list
