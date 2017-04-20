from django.shortcuts import render
from mongoengine import *
from django.http import HttpResponse
from .models import *
from pymongo import *
import sys
from django.core import serializers
from django.http import JsonResponse
from bson.json_util import dumps
import re
from bson.objectid import ObjectId
import bson
from django.core import serializers
import json
import time
from collections import OrderedDict
import math



############# VIEW FUNCTIONS #####################
def startpage(request):
    print("fucking starpage")
    return render(request, "startpage.html")


##Queries and renders a recipe when a recipe in the result list is clicked##
def presentRecipe(request):
    print("present recipe: ", request.method)
    if request.method == "GET": #When the page is retrieved
        print("present recipe, get request")
        req_id = request.path[-24:] #Extracts the id from the path
        recipe_response = recipe.objects.get(_id = ObjectId(req_id))#Runs query with the request ID
        print(recipe_response.ingredients_complete)

        return render(request, "presenterarecept.html", {"recipe": recipe_response})

##Queries user inputs on database and renders a result list##
def retrieveRecipes(request):
    if request.method == "GET":
        raw_input = request.path[17:].split("&") #splits into array based on &, title() makes first letters capitalized (to be reomved?)
        input = []
        for element in raw_input:
            input.append(sanitize(element)) #Sanitizses !! IMPORTANT !!
        ## **COMMENT** ##
        # Now that the input is cleaned, we can implement elasticsearch/fuzzy search on food_ref t
        q1 = mapped.objects(id__in=input).only('value')#.item_frequencies('value')
        print("q1: ", q1)
        #x[1]['frequency']/x[1]['ing_count'] *
        query_mapped = mapped.objects(id__in=input).only('value').key_frequency()#queries from the mapped colletion and does a key_frequency check
        sorted_list = OrderedDict(reversed(sorted(query_mapped.items(), key=lambda x: (x[1]['frequency'], x[1]['clicks'], x[1]['rating'])))) #Sorts list based on frequency
        return render(request, "recipes.html", {"recipe_array": sorted_list})
    else:
        return render(request, "startpage.html")

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
    user_string = re.sub("_", " ", user_string)  # Converts underscore to whitespace
    user_string = re.sub("[^a-öA-Ö],[^-]","", user_string) #removes non alphabetic characters but allows whitespcae and single dash
    user_string = re.sub("--", "", user_string)#removes double dash to prevent injections
    return user_string




