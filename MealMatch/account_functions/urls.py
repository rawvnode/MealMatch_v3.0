from . import views
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin


app_name = 'account_functions'

urlpatterns = [

    #url(r'^update_table', views.update_table, name = "updateTable"),
    #url(r'^delete_field', views.delete_field, name = "deleteTable"),
    #url(r'^logout', views.user_logout, name = "logout"),
    url(r'^logout', views.logout_view, name = "logout"),
    url(r'^create_user', views.register_view, name = "newUser"),

    #url(r'^update_table', views.update_table, name = "updateTable"),
    #url(r'^delete_field', views.delete_field, name = "deleteTable"),
    #url(r'^logout', views.user_logout, name = "logout"),
    url(r'^my_pantry', views.my_pantry, name = "myPantry"),
    url(r'^', views.login_view, name="loginPage"),





]