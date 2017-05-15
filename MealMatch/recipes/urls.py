from django.conf.urls import url

from . import views


urlpatterns = [

    url(r'^recipes/(?P<raw_input>[A-Za-z]{1,75})', views.retrieveRecipes, name="recipes"),
    url(r'^recipes/(?P<recipe_id>(.*){12})', views.presentRecipe, name="recipes"),



    url(r'^autocorrect', views.autocorrect, name="autocorrect"),
    url(r'^presenterarecept/starrating', views.starrating, name="starrating"),
    url(r'^presenterarecept/', views.presentRecipe, name="presenterarecept"),

    url(r'^starrating', views.starrating, name="starrating"),
    #url(r'^refresh', views.refresh, name="refresh"),


    url(r'^$', views.startpage, name = "startpage" ), #VIKTIGT ATT DENNA ÄR SIST

    #url(r'^recipe_match', views.recipes, name="recipe_match"),


    ]