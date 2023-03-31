from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def customPaginator(request, queryset, results):
    page = request.GET.get('page')
    pagination = Paginator(queryset, results)

    try:
        queryset = pagination.page(page)
    except PageNotAnInteger:
        page = 1
        queryset = pagination.page(page)
    except EmptyPage:
        page = pagination.num_pages
        queryset = pagination.page(page)

    leftIndex = (int(page) - 1)
    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page) + 4)
    if rightIndex > pagination.num_pages:
        rightIndex = pagination.num_pages + 1

    custom_range = range(leftIndex, rightIndex)

    return page, custom_range, queryset
