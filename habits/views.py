from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignupForm, LoginForm
from .models import Sololingo, ProgressLog
import random
from datetime import date, timedelta

from solana.account import Account
from solana.rpc.api import Client
from solana.transaction import Transaction
from solana.system_program import transfer

solana_system_wallet = 'DpFELfY8kYLdxADx8X2D2jMANxFCH812XEjtrSteHg1C'
def send_sols(quanity: float):
    # Define sender and receiver wallet addresses
    sender_address = "<SENDER_ADDRESS>"
    receiver_address = "<RECEIVER_ADDRESS>"

    # Define the sender's private key (assuming it's a string)
    sender_private_key = "<SENDER_PRIVATE_KEY>"

    # Connect to Solana Devnet RPC endpoint
    rpc_endpoint = "https://api.devnet.solana.com"
    client = Client(rpc_endpoint)

    # Load sender's account
    sender_account = Account(sender_private_key)

    # Fetch recent blockhash
    blockhash = client.get_recent_blockhash()

    # Create transaction
    transaction = Transaction().add(
        transfer(
            sender_address,
            receiver_address,
            1000000000,  # Amount to send (in lamports, 1 SOL = 1e9 lamports)
        )
    )

    # Sign transaction
    signed_transaction = transaction.sign([sender_account])

    # Send transaction
    tx_hash = client.send_transaction(signed_transaction)
    print("Transaction sent with hash:", tx_hash)

def check_unbilled(user):

    helper_first_payment = 0.01
    current_date = date.today()
    yesterday = current_date - timedelta(days=1)
    print(current_date, yesterday)
    #check uncompleted yesterday
    progress = ProgressLog.objects.filter(user_id=user.id).filter(date=yesterday).exclude(billed=True).exclude(completed=True)
    if len(progress)==1:
        print(f'lets motivate {user.username}-helper is {user.userprofile.address}')


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
