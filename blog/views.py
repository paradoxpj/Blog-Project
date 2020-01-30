from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout

from .forms import SignUpForm, LoginForm

from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    user = request.user
    context = {
        'name': user.username
    }
    return render(request, 'home.html', context)


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
