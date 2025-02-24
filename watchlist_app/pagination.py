from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination


class WatchListCuPagination(CursorPagination):
    page_size = 3
    cursor_query_param = 'record'

# class WatchListLOPagination(LimitOffsetPagination):
#     default_limit = 4
#     max_limit = 10
#     limit_query_param = 'limit'
#     offset_query_param = 'start'
      

# class WatchListPagination(PageNumberPagination):
#     page_size = 3
#     page_query_param = 'p'
#     page_size_query_param = 'size'
#     max_page_size = 10
#     last_page_strings = 'end'