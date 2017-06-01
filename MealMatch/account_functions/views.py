from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from mongoengine.django.auth import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from mongoengine import *
from .forms import *
from django.http import HttpResponseRedirect

from .decorators import check_recaptcha
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime, date
from bson.json_util import dumps

from recipes.models import *
from account_functions.models import *
import re

from account_functions.context_processors import *




##################### for autocorrect


from bson.json_util import dumps
from collections import OrderedDict
from bson.objectid import ObjectId


#####################



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
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



    #return render("startpage.html", {"form": form, "title" : title})
@check_recaptcha
def register_view(request):
    next = request.GET.get('next')
    title = "Register"
    form = UserRegisterForm(request.POST or None)

    if form.is_valid() and request.recaptcha_is_valid:
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
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

### Add recipe functions ####


@login_required(redirect_field_name = "account_functions/login.html")
def admin_page(request):
    # funktioner till admin
    return

@login_required(redirect_field_name = "account_functions/login.html")
def user_page(request):
    # funktioner till vanlig användare
    return

def split_string_ingridients(string):
    list = string.split(":")
    return list

def split_string_directions(string):
    list = string.split(".")
    return list

#@login_required(redirect_field_name = "account_functions/add_recipe.html")


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
        #user = get_user(request)
        mongouser = Profile.objects.get(user_id_reference=request.user.id)
        author = mongouser.full_name
        title_recipe = form.cleaned_data.get('title')
        ingredients = handle_bad_input_from_users(form.cleaned_data.get('ingredients'))

        preperation_time = form.cleaned_data.get('preperation_time')
        #servings = form.check_username('servings')
        directions_recipe = handle_bad_input_from_users(form.cleaned_data.get('directions'))
        #amount = form.check_username('amount')

        category_recipe = handle_bad_input_from_users(form.cleaned_data.get('category'))
        picture_url = form.cleaned_data.get('picture_url')



        ingredients_list = []
        for input in ingredients: #Goes through all user inputs from the form
            ingredient = input.split(" ") #Splits the inputs in ingredients into array (eg 1 pinch of salt -> [1, pinch, of, salt})
            for item in ingredient:
                print(item, "ITEM")


                try:

                    food = food_ref.objects.get(foods__iexact=item) #try and find a match
                    print(food, "FOOD")
                except:
                    pass #if no match found, don't bother about it
                else:
                    ingredients_list.append(food.foods) #if match found append to ingredients_list

        print("ing_list", ingredients_list)




        #ingredients_list = []
        #temp_list = []
        #for ingredient in ingredients:
        #    for index in range(len(foods)):
        #        if foods[index] is not None:
        #            print(foods[index])
        #            if foods[index].lower() in ingredient or foods[index] in ingredient:
        #                if foods[index] not in ingredients_list:
        #                    temp_list.append(foods[index])
        #
        #    if (len(temp_list) > 0):
        #        ingredients_list.append(max(temp_list, key=len))
        #        temp_list = []




        recipe_saving = recipe(title=title_recipe, directions=directions_recipe, tags=category_recipe, ingredients_complete = ingredients,
                               time = preperation_time, image = picture_url, ingredients_list = ingredients_list, author = author)

        recipe_saving.save()
        recipe_id = recipe_saving.id


        for item in ingredients_list:
            item = item.lower()
            item = item[:1].upper() + item[1:]
            mapped_object = mapped.objects(title=item)
            print(mapped_object[0].title)


            mapped_object[0].update(add_to_set__value=ObjectId(recipe_id))

            mapped_object[0].save()


    return render(request, "account_functions/add_recipe.html", context)

    return redirect("/")


def create_profile(request):
    print(request.POST, "#####################")
    check_picture = request.POST.get('picture', None)
    if (check_picture is None or check_picture == ""):
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        full_name = first_name+last_name
        gender = request.POST['gender']
        birthday = datetime.strptime(request.POST['bday'], "%Y-%m-%d")

        user_id = request.user.id
        #country = request.POST['country']
        picture = 'https://upload.wikimedia.org/wikipedia/en/b/b1/Portrait_placeholder.png'
        current_date = date.today()

        age = (current_date.year - birthday.year - ((current_date.month, current_date.day) < (birthday.month, birthday.day)))


        user_profile = Profile(first_name = first_name, last_name = last_name, full_name = full_name, sex = gender, age = age, user_id_reference = user_id, picture = picture)
        user_profile.save()

        return redirect("/account_functions/my_pantry.html")
    else:
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        full_name = first_name + last_name
        gender = request.POST['gender']
        birthday = datetime.strptime(request.POST['bday'], "%Y-%m-%d")
        picture = request.POST['picture']
        user_id = request.user.id
        # country = request.POST['country']

        current_date = date.today()

        age = (
        current_date.year - birthday.year - ((current_date.month, current_date.day) < (birthday.month, birthday.day)))

        user_profile = Profile(first_name=first_name, last_name=last_name, full_name=full_name, sex=gender, age=age,
                               user_id_reference=user_id, picture=picture)
        user_profile.save()

        return redirect("/account_functions/my_pantry.html")

def update_profile(request):
    check_picture = request.POST.get('picture', None)
    if(check_picture is None):

        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        full_name = first_name+last_name
        gender = request.POST['gender']
        birthday = datetime.datetime.strptime(request.POST['bday'], "%Y-%m-%d")

        user_id = request.user.id
        #user_profile = Profile.objects.get(user_id_reference=user_id)

        current_date = date.today()

        age = (current_date.year - birthday.year - ((current_date.month, current_date.day) < (birthday.month, birthday.day)))
        user_profile = Profile.objects.get(user_id_reference=user_id)
        user_profile.update(first_name=first_name, last_name=last_name, full_name=full_name,gender=gender, age=age)
        user_profile.save()


        return redirect("/account_functions/user_profile.html")

    else:
        picture = request.POST['picture']
        user_id = request.user.id
        user_profile = Profile.objects.get(user_id_reference=user_id)
        user_profile.update(picture = picture)
        user_profile.save()

        return redirect("/account_functions/user_profile.html")

###############HELPER FUNCTIONS################

def sanitize_pantry(list):
    for index in range(len(list)):

        if list[index][-1] == "X":
            list[index] = list[index][:-1]
        list[index] = list[index].replace("\n","")
        list[index] = list[index].replace("  ", "") #RÖR EJ; MAGI

    return list

def user_profile(request):
    mongouser = Profile.objects.get(user_id_reference=request.user.id)
    username = mongouser.full_name
    added_recipes = recipe.objects(author=username)
    return render(request, "account_functions/user_profile.html",{"my_recipes":added_recipes})


##Autocorrect implementation. Must be adjusted to prevent crashed (eg via elasticsearch or fewer queries)##
def autocorrect(request):
    input = sanitize(request.POST['input'])  # gets the user input and sanitizses using sanitize()
    if (len(input) > 0):
        array = []
        foods = food_ref.objects(food__istartswith=input)  # checks if any word starts with the user input
        for element in foods:
            array.append(element.food)  # appends matches to an initially empty array
        array = dumps(array)  # dumps the aray to JSON format
        return JsonResponse(array, safe=False)  # returns a JSONResponse to client-side
    else:
        return render(request, "startpage.html") #if there is no input, do as before

############# HELPER FUNCTIONS #############
def sanitize(user_string):
    if (user_string == ""):
        return False
    user_string = re.sub("_", " ", user_string)  # Converts underscore to whitespace
    user_string = re.sub("[^a-öA-Ö],[^-]","", user_string) #removes non alphabetic characters but allows whitespcae and single dash
    user_string = re.sub("--", "", user_string)#removes double dash to prevent injections
    user_string.capitalize()

    return user_string.capitalize()
