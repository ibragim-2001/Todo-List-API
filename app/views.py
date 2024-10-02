from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import *
from .models import *


class TodosView(APIView):

    def get(self, request):
        """
        Сделать пагинацию максимум 10 туду
        GET /todos?page=1&limit=10
        :param request:
        :return:
        """
        items = TodoItem.objects.all()
        try:
            serializer = TodoItemSerializer(items, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
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

    def delete(self, id):
        try:
            todo = TodoItem.objects.get(pk=id)
            todo.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(data={'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data=serializer.errors, status=status.HTTP_204_NO_CONTENT)
