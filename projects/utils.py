from django.db.models import Q
from .models import Project, Tag
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def projectsPagination(request, projects, results):
    page = request.GET.get("page")
    pagination = Paginator(projects, results)

    try:
        projects = pagination.page(page)
    except PageNotAnInteger:
        page = 1
        projects = pagination.page(page)
    except EmptyPage:
        page = pagination.num_pages
        projects = pagination.page(page)

    leftIndex = (int(page) - 1)
    if leftIndex < 1:
        leftIndex = 1
    rightIndex = (int(page) + 3)
    if rightIndex > pagination.num_pages:
        rightIndex = pagination.num_pages + 1

    custom_range = range(leftIndex, rightIndex)
    return page, custom_range, projects


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
