from django.http import HttpResponse , HttpResponseRedirect
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth 


def Welcome(request):
    return HttpResponse("Welcome to Todoapp")


    
def signupview(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        email = request.POST['email']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            user  = User.objects.create_user(email=email,username=username,password=password1,first_name=first_name)
            user.save()
            return redirect('login')
        else:
            return render(request,'signup.html',{'error':'Passwords do not match'})
   
    return render(request,'signup.html')

def Login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('home')
        else:
            return render(request,'login.html',{'error':"Invalid username or password"})
    return render(request,'login.html')

def homePage(request):
    return render(request,"index.html")