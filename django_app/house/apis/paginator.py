from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class ResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 10
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response({
            'entire counts': self.page.paginator.count,
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'results': data,
        })
