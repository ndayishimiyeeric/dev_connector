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

    leftIndex = (int(page) - 2)
    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page) + 4)
    if rightIndex > pagination.num_pages:
        rightIndex = pagination.num_pages + 1

    custom_range = range(leftIndex, rightIndex)

    return page, custom_range, queryset, pagination.count


# style classes for form fields
input_classes = 'block w-full rounded-md py-1.5 bg-gray-50 border border-gray-300 text-gray-900 text-sm focus:ring-blue-500 focus:border-blue-500 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'
textarea_classes = 'block w-full rounded-md bg-gray-50 border border-gray-300 text-gray-900 text-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 sm:py-1.5 sm:text-sm sm:leading-6'
checkbox_classes = 'w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600'
