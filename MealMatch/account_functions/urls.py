from . import views
from django.conf.urls import url

app_name = 'account_functions'
urlpatterns = [
    url(r'^login', views.login_view, name = "loginPage"),
    url(r'^create_user', views.register_view, name = "newUser"),
    url(r'^update_table', views.update_table, name = "updateTable"),
    url(r'^delete_field', views.delete_field, name = "deleteTable"),
    url(r'^logout', views.user_logout, name = "logout"),




]