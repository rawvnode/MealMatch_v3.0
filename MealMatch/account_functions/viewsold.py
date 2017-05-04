def create_new_user(request):
    if request.method == "POST":
        print(users.objects(username = request.POST['mail']))

        if users.objects(username = request.POST['mail']) ==  None:

            user = users.create_user(request.POST['mail'], request.POST['pwd'])
            user.save()
            create_staff = False
            if create_staff:
                staff = users(username = "agatonvet", is_superuser = True)
                staff.save()
            return HttpResponse('you have created a user')
            #return render(request, "new_user.html")
        else:
            return HttpResponse('username already taken')

    else:

        return render(request, "account_functions/create_user.html")


### old
def login_function(request):
    if request.method == "POST":
        username = request.POST['your_name']
        password = request.POST['pwd']
        user = authenticate(username=username, password=password)

        if user is not None:
            users.backend = 'mongoengine.django.auth.MongoEngineBackend'
            try:
                request.session['user'] = user
                login(request, user)
            except users.DoesNotExist:
                print("error does not exist")
            if user.is_authenticated:
                return render(request, "account_functions/update_table.html")
        else:
            return HttpResponse('login failed')
    else:
        return render(request, "account_functions/login.html")

    login_required(redirect_field_name="account_functions/login.html")

def upload_recipes(request):
    # ladda upp ett recept till databasen
    return
@login_required(redirect_field_name="account_functions/login.html")
def admin_page(request):
    # funktioner till admin
    return
@login_required(redirect_field_name="account_functions/login.html")
def user_page(request):
    # funktioner till vanlig användare
    return
