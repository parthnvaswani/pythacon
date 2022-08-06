from django.contrib.auth import login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import SignupForm
import random
import string

@login_required
def index(request,name):
    return render(request, 'home.html', {'room_name': name})

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

def genrand(request):
    return redirect(f"/{genRoom()}")

def genRoom():
    length = 4
    chars = []
    for i in range(length):
        upper = random.choice(string.ascii_uppercase)
        chars += upper
        lower = random.choice(string.ascii_lowercase)
        chars += lower
        digit = random.choice(string.digits)
        chars += digit
        random.shuffle(chars)
        room_code = "".join(chars)
    return room_code

def home(request):
    return render(request, 'meet.html')