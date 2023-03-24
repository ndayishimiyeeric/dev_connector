from django.db.models import Q
from .models import Profile, Skill
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def profilesPaginator(request, profiles, results):
    page = request.GET.get('page')
    pagination = Paginator(profiles, results)

    try:
        profiles = pagination.page(page)
    except PageNotAnInteger:
        page = 1
        profiles = pagination.page(page)
    except EmptyPage:
        page = pagination.num_pages
        profiles = pagination.page(page)

    leftIndex = (int(page) - 1)
    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page) + 4)
    if rightIndex > pagination.num_pages:
        rightIndex = pagination.num_pages + 1

    custom_range = range(leftIndex, rightIndex)

    return custom_range, profiles


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
