from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

# Create your views here.
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html', {"display" : "none"})
    else:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username = username, password = password)
        print("user checked")
        if user is None:
            print("user not logged")
            return render(request, "login.html", {"message" : "check the username or password!", "display" : "block"})
        else:
            print("user logged")
            auth_login(request, user)
            return redirect('/')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if User.objects.filter(username = username).exists():
            return render(request, 'register.html', {"message" : "username already exists!", "display" : "block"})

        if User.objects.filter(email = email).exists():
            return render(request, 'register.html', {"message" : "email is taken!", "display" : "block"})
            
        if password1 == password2:
            user = User.objects.create_user(username=username, first_name=firstname, last_name=lastname, email=email, password=password1)
            user.save()
            return redirect('login')
        else:
            return render(request, "register.html", {"message" : "passwords doesn't match!", "display" : "block"})
    else:
        return render(request, 'register.html', {"display" : "none"})

def logout(request):
    auth_logout(request)
    return redirect("/")