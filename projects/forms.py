from django.forms import ModelForm
from django import forms
from .models import Project, Review, Tag
from constants.utils import input_classes, textarea_classes, checkbox_classes


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

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name != 'project_image' or name != 'tags' or name != 'description':
                field.widget.attrs.update({'class': input_classes})
            if name == 'project_image':
                field.widget.attrs.update({'accept': 'image/*'})
                field.widget.attrs.update({'class': 'sr-only'})
            if name == 'description':
                field.widget.attrs.update({'class': textarea_classes})
            if name == 'tags':
                field.widget.attrs.update({'class': checkbox_classes, 'type': 'checkbox'})


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
