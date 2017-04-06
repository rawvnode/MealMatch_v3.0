"""MealMatch URL Configuration
"""
from django.conf.urls import include, url

urlpatterns = [
    url(r'^recipes/', include("recipes.urls")),
    url(r'^account_functions/', include("account_functions.urls")),
    url(r'^', include("recipes.urls"))
]

