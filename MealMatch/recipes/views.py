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


#from urlparse import urljoin




def test_(request):
    print("startpage")


    recipes = recipe.objects.get()
    all = ""
    for i in recipes.payload:
        print( i, recipes.payload[i])
    return HttpResponse(all)


def startpage(request):
    return render(request, "startpage.html")


def sanitize(user_string):
    user_string = re.sub("[^a-öA-Ö],[^-]," "","", user_string) #removes non alphabetic characters but allows whitespcae and single dash
    user_string = re.sub("--", "", user_string)#removes double dash to prevent injections
    return user_string




def stripAndObjectify(result): #Strips the data from bad formatting (mongoengine bug?) and sets it to an object id

    result = result[8:]
    result = result.strip('("")')

    result = bson.objectid.ObjectId(result)

    return result

def queryMapped(item): #Returns a query from the mapped collection. Matches icontaint on the id field of mapped collection
    return mapped.objects.get(id__icontains=item)




def recipes(request):
    #print(request.COOKIES.get('input').split(',')) #Splits the cookies up (which comes as a string) into an array
    #-- remember to sanitize the list before request is sent to sever
    input = request.COOKIES.get('input').split(',')

    arr = []
    recipe_array = []
    for item in input:
        arr.append(queryMapped(item))


    #Intesect-funktioner etc


    for object in arr:
        temp_array = list(object.value.keys())

        for index in range(len(temp_array)):
            temp_array[index] = stripAndObjectify(temp_array[index])

        recipe_array.append(temp_array)
        temp_array = []

    #print(recipe_array)


    #print(type(result))



########################
    #recipe_query = recipe.objects.get(id =result)
    #print(recipe_query.title)


##################
    #for rec in recipe.objects:
        #print(type(rec.id))

    #recipe_query = recipe.objects.get(title__icontains = result)
    #print(recipe_query)

    #for item in foods_query:
     #   print(item.value)


    return render(request, "recipes.html")

def autocorrect(request):
    input = sanitize(request.POST['input']) #gets the user input and sanitizses using sanitize()
    array = []
    if (len(input) > 0):
        foods = food_ref.objects(food__istartswith=input) #checks if any word starts with the user input
        for element in foods:
            array.append(element.food) #appends matches to an initiall empty array

        array = dumps(array)#dumps the aray to JSON format
        return JsonResponse(array, safe=False) #returns a JSONResponse to client-side
    else:
        return render(request, "startpage.html") #if there is no input, do as before




