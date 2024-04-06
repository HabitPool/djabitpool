from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignupForm, LoginForm
from .models import Sololingo
import random

def index(request):
    template = loader.get_template("habits/index.html")
    return HttpResponse(template.render({}, request))

def sololingo_game(request):
    words = Sololingo.objects.all()
    random_word = random.choice(words)
    options = list(Sololingo.objects.exclude(id=random_word.id).order_by('?')[:2])
    options.append(random_word)
    random.shuffle(options)
    context = {
        'word': random_word,
        'options': options,
    }
    return render(request, 'habits/sololingo_game.html', context)

# signup page
def user_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'habits/signup.html', {'form': form})

# login page
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'habits/login.html', {'form': form})

# logout page
def user_logout(request):
    logout(request)
    return redirect('login')
