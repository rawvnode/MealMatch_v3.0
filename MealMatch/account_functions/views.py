from django.shortcuts import render, redirect
from django.http import HttpResponse
from mongoengine.django.auth import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from mongoengine import *
from .forms import *
from django.http import HttpResponseRedirect

from recipes.models import recipe

#@login_required(redirect_field_name = "account_functions/login.html")
#def delete_field(request):
#    if request.method == "POST":
#        users.objects(username= request.POST['your_name']).delete()
#        return render(request, "account_functions/delete_field.html")
#    else:
#        return render(request, "account_functions/delete_field.html")
#
#
#@login_required(redirect_field_name = "account_functions/login.html")
#def update_table(request):   #change profile settings
#    if request.method == "POST":
#        users.objects(username =  request.POST['old_name']).update(set__username = request.POST['new_name'])
#        return HttpResponse("You renamed your account to:",request.POST['new_name'] )
#    else:
#        return render(request,"account_functions/update_table.html")


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




def my_pantry(request):
    return render(request,"account_functions/my_pantry.html")



def login_view(request):


    title = "Login"
    form = UserLoginForm(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username = username, password = password)

        login(request, user)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


    #return render("startpage.html", {"form": form, "title" : title})

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
def handle_bad_input_from_users(bad_string):
    good_string = bad_string.split(":")
    return good_string
#@login_required(redirect_field_name = "account_functions/add_recipe.html")
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


