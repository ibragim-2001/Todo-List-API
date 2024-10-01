from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import TodoItem
from .serializers import TodoItemSerializer


class Todos(APIView):

    def get(self, request):
        items = TodoItem.objects.all()
        serializer = TodoItemSerializer(items)
        return Response(data=serializer.data, status=status.HTTP_200_OK)