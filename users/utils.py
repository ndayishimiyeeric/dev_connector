from django.db.models import Q
from .models import Profile, Skill


def searchProfiles(request):
    search_query = ''

    if request.GET.get('query'):
        search_query = request.GET.get('query')

    skills = Skill.objects.filter(name__icontains=search_query)
    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=search_query) |
        Q(headline__icontains=search_query) |
        Q(skill__in=skills)
    )

    return search_query, profiles
