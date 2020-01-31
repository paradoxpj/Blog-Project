from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User

from .forms import SignUpForm, LoginForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView

from .models import Post

from django.urls import reverse

from datetime import datetime

from django.db.models import Q



def login_view(request):
    user = request.user
    if user.is_authenticated:
        return redirect('blog:home')
    next = request.GET.get('next')
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        login(request, user)

        if next:
            return redirect(next)
        return redirect('blog:home')
    context = {
        'form': form,
    }
    return render(request, 'login.html', context)


def signup_view(request):
    user = request.user
    if user.is_authenticated:
        return redirect('blog:home')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('blog:home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('blog:login')


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'description', 'image',]
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.created_on = datetime.now()
        return super().form_valid(form)
    def get_success_url(self):
        return reverse('blog:home')


@login_required
def home(request):
    user = request.user
    posts = Post.objects.filter(user=user)
    context = {
        'posts' : posts,
        'user': user,
    }
    return render(request, 'home.html', context)


@login_required
def searchusers(request):
    if request.method == 'GET':
        query= request.GET.get('q')

        submitbutton= request.GET.get('submit')

        if query is not None:
            lookups= Q(username__icontains=query)

            results= User.objects.filter(lookups).distinct()

            context={'searched_user': results,
                     'submitbutton': submitbutton,
                     'title' : 'Search results'
            }

            return render(request, 'search_results.html', context)

        else:
            return render(request, 'search_results.html')

    else:
        return render(request, 'search_results.html')


@login_required
def profile_view(request, user_id):
    searched_user = User.objects.get(pk=user_id)
    posts = Post.objects.filter(user=searched_user)
    context = {
        'posts': posts,
        'searched_user': searched_user
    }
    return render(request, 'profile_view.html', context)
