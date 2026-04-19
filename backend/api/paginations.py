from rest_framework.pagination import PageNumberPagination

from users_backend.constants import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE


class LimitPageNumberPagination(PageNumberPagination):
    """Page numbering with page and limit parameters."""

    page_size = DEFAULT_PAGE_SIZE
    page_query_param = "page"
    page_size_query_param = "limit"
    max_page_size = MAX_PAGE_SIZE
