from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate

from .forms import SignUpForm

from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    user = request.user
    context = {
        'name': user.username
    }
    return render(request, 'home.html', context)


def signup(request):
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
