from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import *
from .models import *
from .services.custom_pagination import CustomPagination


class TodosView(APIView):

    def get(self, request):
        items = TodoItem.objects.all()
        paginator = CustomPagination()
        paginated_items = paginator.paginate_queryset(items, request)

        try:
            serializer = TodoItemSerializer(paginated_items, many=True)
            return paginator.get_paginated_response(serializer.data)
        except Exception as e:
            return Response(data={'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data=serializer.errors, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = TodoItemSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response(data={'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TodoItemVIew(APIView):

    def put(self, request, pk):
        try:
            todo = TodoItem.objects.get(pk=pk)
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
            todo = TodoItem.objects.get(pk=pk)
            todo.delete()
            return Response(data={'message': str(f'The task "{todo.title}" successfully deleted')}, status=status.HTTP_204_NO_CONTENT)
        except TodoItem.DoesNotExist:
            return Response(data={'message': 'Todo item not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(data={'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)