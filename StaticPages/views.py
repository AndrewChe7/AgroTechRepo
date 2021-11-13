from django.shortcuts import render, redirect


# Create your views here.
def home_page(request):
    if request.user.is_authenticated:
        return redirect('/marketplace/')
    return render(request, 'index.html')
