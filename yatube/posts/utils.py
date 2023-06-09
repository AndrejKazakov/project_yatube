from django.core.paginator import Paginator

NUMBER_OF_RECORDS = 3


def paginator(request, posts_list):
    paginator = Paginator(posts_list, NUMBER_OF_RECORDS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj
