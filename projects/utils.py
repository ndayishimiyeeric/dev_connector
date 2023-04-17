from django.db.models import Q
from .models import Project, Tag


def searchProjects(request):
    search_query = ''

    if request.GET.get('q'):
        search_query = request.GET.get('q')

    tags = Tag.objects.filter(name__icontains=search_query)
    projects = Project.objects.distinct().filter(
        Q(title__icontains=search_query) |
        Q(description__icontains=search_query) |
        Q(owner__name__icontains=search_query) |
        Q(tags__in=tags)
    )

    return search_query, projects


def userProjects(request):
    profile = request.user.profile
    projects = Project.objects.filter(owner=profile)
    query = ''

    if request.GET.get('query'):
        query = request.GET.get('query')

    # search into user projects
    filtered_projects = projects.distinct().filter(
        Q(title__icontains=query) |
        Q(description__icontains=query) |
        Q(tags__name__icontains=query)
    ).order_by('-updated_at')

    return query, filtered_projects
