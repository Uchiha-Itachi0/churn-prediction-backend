from rest_framework.pagination import PageNumberPagination


class CSVContentPagination(PageNumberPagination):
    page_size = 20  # Default number of items per page
    page_size_query_param = 'page_size'  # Allow custom page size in the query param
    # max_page_size is removed to allow unlimited pagination
