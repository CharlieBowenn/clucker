from django.shortcuts import redirect, render
from .forms import SignUpForm, LogInForm, PostForm
from .models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

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
    form = PostForm()
    return render(request, 'feed.html', {'form': form})

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
        # Error messages go here
        messages.add_message(request, messages.ERROR, "Username/Password are invalid ya dam fool")
    form = LogInForm()
    return render(request, 'log_in.html', {'form': form})

def log_out(request):
    logout(request)
    return redirect('home')

def user_list(request):
    users = User.objects.all()
    userInfo = []
    for user in users:
        userInfo.append(""+user.username+" "+user.first_name+" "+user.last_name)
    context = {'userInfo': userInfo}
    return render(request, 'user_list.html', context)

def show_user(request, user_id):
    chosen = User.objects.get(id=user_id)
    info = []
    info.append('User ID: '+str(chosen.id))
    info.append('Username: '+chosen.username)
    info.append('First name: '+chosen.first_name)
    info.append('Last name: '+chosen.last_name)
    info.append('Email: '+chosen.email)
    context = {'info': info}
    return render(request, 'show_user.html', context)
