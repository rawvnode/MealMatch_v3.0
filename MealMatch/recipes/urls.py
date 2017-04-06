from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.startpage, name = "startpage" ),
    url(r'^recipes', views.recipes, name="recipes"),
    url(r'^autocorrect', views.autocorrect, name="autocorrect"),

    #url(r'^recipe_match', views.recipes, name="recipe_match"),


    ]