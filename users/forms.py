from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django import forms
from django.forms.widgets import PasswordInput, DateInput
from django.contrib.auth.models import User
from .models import Profile, Skill, Experience, Education


class PasswordInput(PasswordInput):
    def __init__(self, attrs=None):
        super().__init__(attrs={'placeholder': '••••••••', **(attrs or {})})


class CustomerUserCreationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'username', 'email', 'password1', 'password2']
        labels = {
            'first_name': 'Name',
        }

        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Full Name'}),
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'email': forms.TextInput(attrs={'placeholder': 'Email'}),
        }


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'username', 'email', 'headline', 'bio',
                  'profile_image', 'location', 'linkedin', 'github',
                  'website', 'twitter', 'youtube']
        labels = {
            'name': 'Name',
            'bio': 'About Me',
            'profile_image': 'Profile Picture',
        }

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Full Name'}),
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'email': forms.TextInput(attrs={'placeholder': 'Email'}),
            'headline': forms.TextInput(attrs={'placeholder': 'Give us an idea of where you are in your career'}),
            'bio': forms.Textarea(attrs={'placeholder': 'Tell us a little about yourself'}),
            'profile_image': forms.FileInput(attrs={'placeholder': 'Upload your profile image'}),
            'location': forms.TextInput(attrs={'placeholder': 'City & state suggested (eg. Boston, MA)'}),
            'linkedin': forms.TextInput(attrs={'placeholder': 'Linkedin URL'}),
            'github': forms.TextInput(attrs={'placeholder': 'Github URL'}),
            'website': forms.TextInput(attrs={'placeholder': 'Website URL'}),
            'twitter': forms.TextInput(attrs={'placeholder': 'Twitter URL'}),
            'youtube': forms.TextInput(attrs={'placeholder': 'YouTube URL'}),
        }


class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'description']

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Skill Name'}),
            'description': forms.Textarea(attrs={'placeholder': 'Skill Description'}),
        }


class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = ['title', 'company', 'location', 'from_date', 'to_date', 'is_current', 'description']

        labels = {
            'from_date': 'From',
            'to_date': 'To',
            'is_current': 'Current Job',
        }

        widgets = {
            'title': forms.TextInput(attrs={'placeholder': '* Job Title'}),
            'company': forms.TextInput(attrs={'placeholder': '* Company Name'}),
            'location': forms.TextInput(attrs={'placeholder': '* City & state suggested (eg. Boston, MA)'}),
            'description': forms.Textarea(attrs={'placeholder': '* Job Description'}),
            'from_date': DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'to_date': DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'is_current': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
