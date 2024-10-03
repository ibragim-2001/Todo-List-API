from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import *
from .models import *


class TodosView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        items = TodoItem.objects.filter(user=request.user)

        paginator = PageNumberPagination()
        paginator.page_size = request.query_params.get('limit', 10)
        result_page = paginator.paginate_queryset(items, request)
        try:
            serializer = TodoItemSerializer(result_page, many=True)
            return paginator.get_paginated_response({
                'data': serializer.data,
                'page': paginator.page.number,
                'limit': paginator.page_size,
                'total': paginator.page.paginator.count,
            })
        except Exception as e:
            return Response(data={'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data=serializer.errors, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = TodoItemSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(user=request.user)
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response(data={'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TodoItemVIew(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, pk):
        try:
            todo = TodoItem.objects.get(pk=pk, user=request.user)
        except TodoItem.DoesNotExist:
            return Response(data={'message': 'Todo item not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = TodoItemSerializer(todo, data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response(data={'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data=serializer.errors, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, pk):
        try:
            todo = TodoItem.objects.get(pk=pk, user=request.user)
            todo.delete()
            return Response(data={'message': str(f'The task "{todo.title}" successfully deleted')}, status=status.HTTP_204_NO_CONTENT)
        except TodoItem.DoesNotExist:
            return Response(data={'message': 'Todo item not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(data={'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)