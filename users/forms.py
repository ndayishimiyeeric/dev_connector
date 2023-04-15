from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django import forms
from django.forms.widgets import PasswordInput, DateInput
from django.contrib.auth.models import User
from .models import Profile, Skill, Experience, Education

# style classes for form fields
input_classes = 'block w-full rounded-md py-1.5 bg-gray-50 border border-gray-300 text-gray-900 text-sm focus:ring-blue-500 focus:border-blue-500 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
textarea = 'block w-full rounded-md bg-gray-50 border border-gray-300 text-gray-900 text-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 sm:py-1.5 sm:text-sm sm:leading-6'
checkbox = 'w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600'


class PasswordInput(PasswordInput):
    def __init__(self, attrs=None):
        super().__init__(attrs={'placeholder': '••••••••',
                                'class': 'block w-full p-2.5 border-0 bg-transparent text-[#ffffff] focus:ring-0',
                                **(attrs or {})})


class CustomerUserCreationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'username', 'email', 'password1', 'password2']
        labels = {
            'first_name': 'Name',
            'password1': 'Create Password',
        }

        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Full Name',
                                                 'class': 'block w-full p-2.5 border-0 bg-transparent text-[#ffffff] focus:ring-0'}),
            'username': forms.TextInput(attrs={'placeholder': 'Username',
                                               'class': 'block w-full p-2.5 border-0 bg-transparent text-[#ffffff] focus:ring-0'}),
            'email': forms.TextInput(attrs={'placeholder': 'Email',
                                            'class': 'block w-full p-2.5 border-0 bg-transparent text-[#ffffff] focus:ring-0'}),
        }


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'username', 'email', 'headline', 'bio',
                  'profile_image', 'location', 'linkedin', 'github',
                  'website', 'twitter', 'youtube']
        labels = {
            'name': 'Name',
            'bio': 'About',
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

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name != 'profile_image':
                field.widget.attrs.update({'class': input_classes})
            if name == 'profile_image':
                field.widget.attrs.update({'accept': 'image/*'})
                field.widget.attrs.update({'class': 'sr-only'})


class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'description']

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Skill Name'}),
            'description': forms.Textarea(attrs={'placeholder': 'Skill Description'}),
        }

    def __init__(self, *args, **kwargs):
        super(SkillForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == 'name':
                field.widget.attrs.update({'class': input_classes})
            if name == 'description':
                field.widget.attrs.update({'class': textarea})
                field.widget.attrs.update({'rows': '3'})


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

    def __init__(self, *args, **kwargs):
        super(ExperienceForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name != 'is_current' or name == 'description':
                field.widget.attrs.update({'class': input_classes})
            if name == 'is_current':
                field.widget.attrs.update({'class': checkbox})
            if name == 'description':
                field.widget.attrs.update({'class': textarea})


class EducationForm(ModelForm):
    class Meta:
        model = Education
        fields = ['school', 'degree', 'field_of_study', 'from_date', 'to_date', 'is_current', 'description']

        labels = {
            'from_date': 'From',
            'to_date': 'To',
            'is_current': 'Current School',
        }

        widgets = {
            'school': forms.TextInput(attrs={'placeholder': '* School Name'}),
            'degree': forms.Select(attrs={'placeholder': '* Degree or Certification'}),
            'field_of_study': forms.TextInput(attrs={'placeholder': '* Field of Study'}),
            'description': forms.Textarea(attrs={'placeholder': '* Description'}),
            'from_date': DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'to_date': DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'is_current': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
