from django.conf import settings
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from .forms import SignUpForm, LogInForm, PostForm
from .models import User, Post
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist, ImproperlyConfigured
from django.http import HttpResponseForbidden, Http404
from .helpers import login_prohibited
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin

# request is simply session ID
@login_prohibited
def home(request):
    return render(request, 'home.html')

@login_prohibited
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

@login_required
def feed(request):
    form = PostForm()
    current_user = request.user
    authors = list(current_user.followees.all()) + [current_user]
    posts = Post.objects.filter(author__in = authors)
    return render(request, 'feed.html', {'form': form, 'user': current_user, 'posts': posts})

# class FeedView(LoginRequiredMixin, ListView):
#     """Class-based generic view for displaying feed"""
#
#     model = Post
#     template_name = 'feed.html'
#     context_object_name = 'posts'
#
#     def get_queryset(self):
#         """Return user's feed"""
#         current_user = self.request.user
#         authors = list(current_user.followees.all()) + [current_user]
#         posts = Post.objects.filter(author__in = authors)
#         return posts
#
#     def get_context_data(self, **kwargs):
#         """Return context data, including new post form"""
#         context = super().get_context_data(**kwargs)
#         context['user'] = self.request.user
#         context['form'] = PostForm()

@login_required
def follow_toggle(request, user_id):
    current_user = request.user
    try:
        followee = User.objects.get(id=user_id)
        current_user.toggle_follow(followee)
    except ObjectDoesNotExist:
        return redirect('user_list')
    else:
        return redirect('show_user', user_id=user_id)

class LoginProhibitedMixin:
    """Mixin that redirects when a user is logged in"""

    redirect_when_logged_in_url = None

    def dispatch(self, *args, **kwargs):
        """Redirect when logged in, or dispatch as normal otherwise"""
        if self.request.user.is_authenticated:
            return self.handle_already_logged_in(*args, **kwargs)
        return super().dispatch(*args, **kwargs)

    def handle_already_logged_in(self, *args, **kwargs):
        url = self.get_redirect_when_logged_in_url()
        return redirect(url)

    def get_redirect_when_logged_in_url(self):
        """Returns url to redirect to when user not logged in"""
        if self.redirect_when_logged_in_url is None:
            raise ImproperlyConfigured("LoginProhibitedMixin requires value for redirect_when_logged_in_url, or an implementation of get_redirect_when_logged_in_url()")
        else:
            return self.redirect_when_logged_in_url

class LogInView(LoginProhibitedMixin, View):
    """View that handles log in"""

    http_method_names = ['get', 'post']
    redirect_when_logged_in_url = 'feed'

    def get(self, request):
        """Display log in template"""
        self.next = request.GET.get('next') or ''
        return self.render()

    def post(self, request):
        """Handle log in attempt"""
        form = LogInForm(request.POST)
        self.next = request.POST.get('next') or settings.REDIRECT_URL_WHEN_LOGGED_IN
        user = form.get_user()
        if user is not None:
            # pass session id and user into django login method
            login(request, user)
            return redirect(self.next)
        # Error messages go here
        messages.add_message(request, messages.ERROR, "Username/Password are invalid ya dam fool")
        return self.render()

    def render(self):
        """Render log in template with blank log in form"""
        form = LogInForm()
        return render(self.request, 'log_in.html', {'form': form, 'next': self.next})


# @login_prohibited
# def log_in(request):
#     if request.method == 'POST':
#         form = LogInForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 # pass session id and user into django login method
#                 login(request, user)
#                 redirect_url = request.POST.get('next') or 'feed'
#                 return redirect(redirect_url)
#         # Error messages go here
#         messages.add_message(request, messages.ERROR, "Username/Password are invalid ya dam fool")
#
#     form = LogInForm()
#     next = request.GET.get('next') or ''
#     return render(request, 'log_in.html', {'form': form, 'next': next})

def log_out(request):
    logout(request)
    return redirect('home')

# @login_required
# def user_list(request):
#     users = User.objects.all()
#     return render(request, 'user_list.html', {'users': users})

class UserListView(LoginRequiredMixin, ListView):
    """View that shows list of all users"""

    model = User
    template_name = "user_list.html"
    context_object_name = "users"

    # @method_decorator(login_required)
    # def dispatch(self, request):
    #     return super().dispatch(request)


# @login_required
# def show_user(request, user_id):
#     try:
#         user = User.objects.get(id=user_id)
#         posts = Post.objects.filter(author=user)
#         following = request.user.is_following(user)
#         followable = (request.user != user)
#     except ObjectDoesNotExist:
#         return redirect('user_list')
#     else:
#         return render(request, 'show_user.html', {'user': user, 'posts': posts, 'following': following, 'followable': followable})

class ShowUserView(DetailView):
    """View that shows individual user details"""
    model = User
    template_name = 'show_user.html'
    context_object_name = "user"
    pk_url_kwarg = 'user_id'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        """Generate content to be displayed in a template"""

        context = super().get_context_data(*args, **kwargs)
        user = self.get_object()
        context['posts'] = Post.objects.filter(author=user)
        context['following'] = self.request.user.is_following(user)
        context['followable'] = (self.request.user != user)
        return context

    def get(self, request, *args, **kwargs):
        """Handle get request, redirect to user_list if user_id invalid"""

        try:
            return super().get(request, *args, **kwargs)
        except Http404:
            return redirect('user_list')

def new_post(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            current_user = request.user
            form = PostForm(request.POST)
            if form.is_valid():
                text = form.cleaned_data.get('text')
                post = Post.objects.create(author=current_user, text=text)
                return redirect('feed')
            else:
                return render(request, 'feed.html', {'form': form})
        else:
            return redirect('log_in')
    else:
        return HttpResponseForbidden()
