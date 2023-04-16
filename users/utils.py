from django.db.models import Q
from .models import Profile, Skill
from projects.models import Project


def searchProfiles(request):
    search_query = ''

    if request.GET.get('q'):
        search_query = request.GET.get('q')

    skills = Skill.objects.filter(name__icontains=search_query)
    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=search_query) |
        Q(headline__icontains=search_query) |
        Q(skill__in=skills)
    )

    return search_query, profiles


def searchUserProjects(request):
    profile = Profile.objects.get(id=request.user.profile.id)
    userProjects = Project.objects.filter(owner=profile)
    query = ''

    if request.GET.get('query'):
        query = request.GET.get('query')

    # search into user projects
    projects = userProjects.distinct().filter(
        Q(title__icontains=query) |
        Q(description__icontains=query) |
        Q(tags__name__icontains=query)
    ).order_by('-updated_at')

    return query, projects
