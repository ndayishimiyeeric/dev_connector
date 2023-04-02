from django.forms import ModelForm
from django import forms
from .models import Project, Review, Tag


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'project_image', 'source_code', 'live_preview', 'tags']

        widgets = {
            'title': forms.TextInput(attrs={'placeholder': '* Project title'}),
            'description': forms.Textarea(attrs={'cols': 30, 'rows': 5, 'placeholder': '* Project Description'}),
            'source_code': forms.TextInput(attrs={'placeholder': 'Source Code'}),
            'live_preview': forms.TextInput(attrs={'placeholder': 'Live Preview'}),
            'tags': forms.CheckboxSelectMultiple(),
        }


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value', 'body']

        labels = {
            'value': 'Vote',
            'body': 'Comment',
        }

        widgets = {
            'body': forms.Textarea(attrs={'cols': 30, 'rows': 5, 'placeholder': 'Leave a comment'}),
        }
