from django.core.paginator import Paginator
import math

# def make_pagination(request, queryset, per_page):
#     try:
#         current_page_number = int(request.GET.get('page', 1))
#     except ValueError:
#         current_page_number = 1

#     queryset = queryset.order_by('-id')

#     paginator = Paginator(queryset, per_page)
#     current_page = paginator.get_page(current_page_number)

#     total_pages = paginator.num_pages

#     # Definir o número máximo de páginas a serem exibidas antes e depois da página atual
#     max_pages_displayed = 5
#     half_max_pages_displayed = max_pages_displayed // 2

#     if total_pages <= max_pages_displayed:
#         start_range = 1
#         end_range = total_pages
#     elif current_page_number <= half_max_pages_displayed:
#         start_range = 1
#         end_range = max_pages_displayed
#     elif current_page_number >= total_pages - half_max_pages_displayed:
#         start_range = total_pages - max_pages_displayed + 1
#         end_range = total_pages
#     else:
#         start_range = current_page_number - half_max_pages_displayed
#         end_range = current_page_number + half_max_pages_displayed

#     first_page_out_of_range = current_page_number > half_max_pages_displayed
#     last_page_out_of_range = end_range < total_pages - half_max_pages_displayed

#     pagination_range = range(start_range, end_range + 1)
    
#     query_string = request.GET.urlencode()

#     return current_page, {
#         'pagination_range': pagination_range,
#         'total_pages': total_pages,
#         'first_page_out_of_range': first_page_out_of_range,
#         'last_page_out_of_range': last_page_out_of_range,
#         'current_page': current_page_number,
#         'query_string': query_string,  # Passando a query string para o template
#     }


def make_pagination(request, queryset, per_page):
    try:
        current_page_number = int(request.GET.get('page', 1))
    except ValueError:
        current_page_number = 1

    queryset = queryset.order_by('-id')

    paginator = Paginator(queryset, per_page)
    current_page = paginator.get_page(current_page_number)

    total_pages = paginator.num_pages

    max_pages_displayed = 5
    half_max_pages_displayed = max_pages_displayed // 2

    if total_pages <= max_pages_displayed:
        start_range = 1
        end_range = total_pages
    elif current_page_number <= half_max_pages_displayed:
        start_range = 1
        end_range = max_pages_displayed
    elif current_page_number >= total_pages - half_max_pages_displayed:
        start_range = total_pages - max_pages_displayed + 1
        end_range = total_pages
    else:
        start_range = current_page_number - half_max_pages_displayed
        end_range = current_page_number + half_max_pages_displayed

    first_page_out_of_range = current_page_number > half_max_pages_displayed
    last_page_out_of_range = end_range < total_pages - half_max_pages_displayed

    pagination_range = range(start_range, end_range + 1)

    # Construir a query string excluindo todos os parâmetros "page" existentes
    query_params = request.GET.copy()
    query_params.pop('page', None)
    query_string = query_params.urlencode()

    return current_page, {
        'pagination_range': pagination_range,
        'total_pages': total_pages,
        'first_page_out_of_range': first_page_out_of_range,
        'last_page_out_of_range': last_page_out_of_range,
        'current_page': current_page_number,
        'query_string': query_string,
    }