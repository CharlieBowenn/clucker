from django.shortcuts import redirect, render
from .forms import SignUpForm, LogInForm
from .models import User
from django.contrib.auth import authenticate, login

# request is simply session ID
def home(request):
    return render(request, 'home.html')

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('feed')
    else:
        form = SignUpForm()
    return render(request, 'sign_up.html', {'form': form})

def feed(request):
    return render(request, 'feed.html')

def log_in(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                # pass session id and user into django login method
                login(request, user)
                return redirect('feed')
    form = LogInForm()
    return render(request, 'log_in.html', {'form': form})
