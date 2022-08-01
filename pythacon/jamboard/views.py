from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import SignupForm

def index(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = SignupForm()
        
    return render(request, 'signup.html', {'form': form})