from rest_framework.pagination import PageNumberPagination


class StandardResultsPagination(PageNumberPagination):
    """
    Custom pagination class for review listings.
    Default page size: 8 (matches frontend expectations)
    Max page size: 100 (prevents excessive server load)
    """
    page_size = 8
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        """
        Custom paginated response format with additional metadata
        """
        response = super().get_paginated_response(data)
        response.data.update({
            'current_page': self.page.number,
            'total_pages': self.page.paginator.num_pages,
            'page_size': self.get_page_size(self.request),
            'total_items': self.page.paginator.count
        })
        return response
