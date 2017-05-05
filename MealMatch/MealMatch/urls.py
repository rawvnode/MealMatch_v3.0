"""MealMatch URL Configuration
"""
from django.conf.urls import include, url
from rest_framework_mongoengine import routers
from django.contrib import admin

# from MealMatch.recipes.viewsets import viewsets
from recipes.viewsets import *

router = routers.DefaultRouter()

### here we register the different api sites ###
router.register(r'recipe', recipeViewSet,r"recipe")
router.register(r'mapped', mappedViewSet,r"mapped")

urlpatterns = [

    ##main application urls
    url(r'^recipes/', include("recipes.urls")),
    url(r'^about/', include("contact.urls")),
    url(r'^account_functions/', include("account_functions.urls", namespace = "account_functions")),
    url(r'^', include("recipes.urls")), #varför har vi två länkar som inklucerar recipes?

    ##API urls
    url(r'^api/', include(router.urls, namespace = 'api') ),

    ##social
    url(r'^oauth/', include('social_django.urls', namespace='social')),  # <--


    ##admin
    url(r'^admin/', include(admin.site.urls)),


]


LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = 'recipes'