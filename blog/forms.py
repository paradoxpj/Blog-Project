from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class SignUpForm(UserCreationForm):


    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', )


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Username'}),)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password'}))
    def clean(self, *args, **kwargs):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('Invalid Username or Password')
            if not user.check_password(password):
                raise forms.ValidationError('Wrong Password')
            if not user.is_active:
                raise forms.ValidationError('not active')
        return super(LoginForm, self).clean(*args, **kwargs)
