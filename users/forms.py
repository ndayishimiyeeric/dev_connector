from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms.widgets import PasswordInput
from django.contrib.auth.models import User



class PasswordInput(PasswordInput):
    def __init__(self, attrs=None):
        super().__init__(attrs={'placeholder': '••••••••', **(attrs or {})})

class CustomerUserCreationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=PasswordInput)
    class Meta:
        model = User
        fields = ['first_name','username', 'email', 'password1', 'password2']
        labels = {
            'first_name': 'Name',
        }

        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Full Name'}),
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'email': forms.TextInput(attrs={'placeholder': 'Email'}),
        }
