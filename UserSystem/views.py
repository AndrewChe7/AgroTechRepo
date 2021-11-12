from django.shortcuts import render, redirect
from django.contrib.auth.models import User, UserManager
from UserSystem.models import UserInfo, UserTypes
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def registration(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        try:
            user_type = int(request.POST['user_type'])
        except ValueError:
            return redirect('/register')
        new_user = User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name)
        new_user_info = UserInfo.objects.create(user=new_user, user_type=user_type)
        new_user.save()
        new_user_info.save()
        return redirect('/auth/login/')
    return render(request, 'registration.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'login.html', context={'is_error': True})
    return render(request, 'login.html', context={'is_error': False})


def logout_view(request):
    logout(request)
    return redirect('/auth/login/')
