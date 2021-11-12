from django.shortcuts import render, redirect
from django.contrib.auth.models import User, UserManager
from UserSystem.models import UserInfo, UserTypes


# Create your views here.
def registration (request):
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
        return redirect('/')
    return render(request, 'registration.html')


def login(request):
    return render(request, 'login.html')
