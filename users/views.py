from django.shortcuts import render
from .models import Profile

# Create your views here.

def profiles(request):
    profiles = Profile.objects.all()
    context = {
        'profiles': profiles
    }
    return render(request, 'users/profiles.html', context)

def profile(request, pk):
    obj = Profile.objects.get(id=pk)
    mainSkills = obj.skill_set.exclude(description__exact="")
    otherSkills = obj.skill_set.filter(description__exact="")

    # query all experiences sorted by is_current and then by to_date
    experiences = obj.experience_set.all().order_by('-is_current', '-to_date')

    # query all educations sorted by is_current and then by to_date
    educations = obj.education_set.all().order_by('-is_current', '-to_date')
    context = {
        'profile': obj,
        'mainSkills': mainSkills,
        'otherSkills': otherSkills,
        'experiences': experiences,
        'educations': educations
    }
    return render(request, 'users/profile.html', context)
