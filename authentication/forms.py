
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms


class LoginForm(forms.Form):
    username=forms.CharField(max_length=50,label="username")
    password=forms.CharField(max_length=20,widget=forms.PasswordInput,label="password")


class SingupUserForm(UserCreationForm):
    password1=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control mt-2","placeholder":"enter your password"}),
                              required=True,
                              label="Password")
    password2=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control mt-2","placeholder":"confirm your password"}),
                              required=True,
                              label="confirm password")
    class Meta(UserCreationForm.Meta):
        model= get_user_model()
        fields=['first_name','last_name','username','email']
        labels={
            'username':""
        }
        widgets ={
            "username":forms.widgets.TextInput(attrs={"class":"form-control mt-2","placeholder":"enter your username"},),
            "first_name":forms.widgets.TextInput(attrs={"class":"form-control mt-2","placeholder":"enter your first name"}),
            "email":forms.widgets.EmailInput(attrs={"class":"form-control mt-2","placeholder":"enter your email"}),
            "last_name":forms.widgets.TextInput(attrs={"class":"form-control mt-2","placeholder":"enter your last name"}),
        }
