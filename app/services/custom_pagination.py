from rest_framework.pagination import BasePagination
from rest_framework.response import Response


class CustomPagination(BasePagination):
    def paginate_queryset(self, queryset, request, view=None):
        self.request = request

        limit = int(request.query_params.get('limit', 10))
        page = int(request.query_params.get('page', 1))
        start = (page - 1) * limit
        end = start + limit
        self.total = queryset.count()
        return list(queryset[start:end])

    def get_paginated_response(self, data):
        return Response({
            'data': data,
            'page': int(self.request.query_params.get('page', 1)),
            'limit': int(self.request.query_params.get('limit', 10)),
            'total': self.total,
        })