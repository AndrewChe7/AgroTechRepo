from django.shortcuts import render, redirect
from django.contrib.auth.models import User, UserManager
from UserSystem.models import UserInfo, UserTypes
from django.contrib.auth import authenticate, login, logout
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


# Create your views here.
def registration(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        bad_username = False
        bad_email = False
        bad_type = False
        username = request.POST['username']
        if User.objects.filter(username=username).exists():
            bad_username = True
        password = request.POST['password']
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            bad_email = True
        try:
            validate_email(email)
        except ValidationError:
            bad_email = True
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        user_type = 0
        try:
            user_type = int(request.POST['user_type'])
        except ValueError:
            bad_type = True
        if bad_email or bad_type or bad_username:
            return render(request, 'registration.html', context={'bad_email': bad_email,
                                                                 'bad_username': bad_username,
                                                                 'bad_type': bad_type,
                                                                 'first_load': False})
        new_user = User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name)
        new_user_info = UserInfo.objects.create(user=new_user, user_type=user_type)
        new_user.save()
        new_user_info.save()
        return redirect('/auth/login/')
    return render(request, 'registration.html', context={'first_load': True})


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
