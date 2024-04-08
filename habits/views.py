from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignupForm, LoginForm
from .models import Sololingo, ProgressLog
import random
from datetime import date, timedelta
from .pylana import transfer_coins

solana_system_wallet = 'DpFELfY8kYLdxADx8X2D2jMANxFCH812XEjtrSteHg1C'
def send_sols(quanity: float):
    # Define sender and receiver wallet addresses
    sender_private_address = "ddc3d3d2d3c7a2fdee21a41179d1261abacd83b6db35d9cc6268a675cc330261"
    helper_public_address = "C9sEuchVeE5vbqGA1zaZDKsngERuc9jTVEbLJBVBagTt"


def check_unbilled(user):

    helper_first_payment = 0.01
    current_date = date.today()
    yesterday = current_date - timedelta(days=1)
    preyesterday = current_date - timedelta(days=2)
    print(current_date, yesterday)
    #check uncompleted yesterday
    current_user = ProgressLog.objects.filter(user_id=user.id)
    if current_user.filter(date=yesterday).filter(completed=True).filter(billed=False).exists() and current_user.filter(date=preyesterday).filter(completed=False).filter(billed=True).exists():
        pass #it seems heler was effective and we send salary
    if current_user.filter(date=yesterday).filter(completed=False).filter(billed=False):
        pass
        print(f'lets motivate {user.username}-helper is {user.userprofile.helper_address}')


    progress = ProgressLog.objects.filter(user_id=user.id).exclude(billed=True).exclude(completed=True)
    for obj in progress:
        print(obj.date, obj.completed)

def index(request):
    check_unbilled(request.user)
    template = loader.get_template("habits/index.html")
    progress = (ProgressLog.objects.filter(user_id=request.user.id))
    print(f' records {len(progress)}')

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
