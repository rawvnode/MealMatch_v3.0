from django.shortcuts import render
from mongoengine import *
from django.http import HttpResponse
from .models import *
import pymongo
import sys
from django.core import serializers
from django.http import JsonResponse
from bson.json_util import dumps

# Create your views here.
def test_(request):
    print("startpage")
    #recipes = Recipe.objects()
    #print(recipes)
    #namn = ""
    #for name in recipe.objects:
     #   namn = namn + " " + name.rating[0]

    recipes = recipe.objects.get()
    all = ""
    #for index in range(len(recipes.payload["directions"])):
        #all ="Step " + str(index + 1) + ": " + recipes.payload["directions"][index]
        #print("\n")
        #print(all)
    for i in recipes.payload:
        print( i, recipes.payload[i])



    return HttpResponse(all)

def startpage(request):
    #print("trump that page")
    foods = food.objects()

    print("Batman is here and ready to serve you, master.")

    food_array = []
    #try: #kolla va' läckert! Kikar om det användaren matat in något i sökrutan för att på så sätt autosuggesta
     #   print(request.POST['input'])
      #  input = (request.POST['input'])
       # foods = food.objects(food__icontains=input)


#        data = serializers.serialize("json", foods)

 #       return JsonResponse(foods)
        #(foods, content_type="application/json")
  #  except:
   #     print("wrong ", sys.exc_info()[0])
    #finally:
    return render(request, "startpage.html")



def recipes(request):
    print(request.COOKIES.get('input'))




    print("halloj")

    return render(request, "recipes.html")

def autocorrect(request):
    print("autocorrect")
    #print(request.POST)
    print(request.COOKIES)
    input = (request.POST['input'])
    foods = food.objects(food__istartswith=input)
    array = []
    for element in foods:
        array.append(element.food)
        #print("food is: ", element.food)
    array = dumps(array)
    #print(type(foods))
    #data = dumps(foods)
    #data = serializers.serialize("json", foods)
    # (foods, content_type="application/json")

    return JsonResponse(array, safe=False)

