from django.db.models import Q
from .models import Project, Tag


def searchProjects(request):
    search_query = ''

    if request.GET.get('query'):
        search_query = request.GET.get('query')

    tags = Tag.objects.filter(name__icontains=search_query)
    projects = Project.objects.distinct().filter(
        Q(title__icontains=search_query) |
        Q(description__icontains=search_query) |
        Q(owner__name__icontains=search_query) |
        Q(tags__in=tags)
    )

    return search_query, projects
