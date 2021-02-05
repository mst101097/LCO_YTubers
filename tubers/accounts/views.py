from django.shortcuts import render , redirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required

# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username = username, password = password)
        
        if user is not None:
            auth.login(request,user)
            messages.error(request,'you are loggedIn')
            return redirect('dashboard')

        else:
            messages.error(request,'Invalid Details ')
            return redirect('login')


    return render(request,"accounts/login.html")


def register(request):
    if request.method =='POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(username = username).exists():
                messages.error(request,'UserName already exists')
                return redirect('register')
            else:
                if User.objects.filter(email = email).exists():
                    messages.error(request,'Email alredy exists')
                    return redirect('register')
                else:
                    user = User.objects.create_user(first_name = firstname, last_name = lastname, username =  username, email = email, password = password)
                    user.save()
                    messages.success(request,'Account created Successfully ')
                    return redirect('login')
        else:
            messages.error(request,'Password Does not match')
            return redirect('register')

    return render(request,"accounts/register.html")


def logout_user(request):
    logout(request)
    return redirect('home')

@login_required(login_url='register')
def dashboard(request):
    return render(request,"accounts/dashboard.html")
