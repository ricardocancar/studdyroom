# import django HttpResponse
from django.shortcuts import HttpResponse
# import rest_framework response

from rest_framework.response import Response

from .serializers import roomSerializer
from rest_framework.views import APIView
from base.models import Room
# Create your views here.

# create a room api view

class roomsView(APIView):
    def get(self, request):
        rooms = Room.objects.all()
        serializer = roomSerializer(rooms, many=True)
        return Response(serializer.data)

# get a single room api view
class roomView(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(id=pk)
        except Room.DoesNotExist:
            return HttpResponse(status=404)
    
    def get(self, request, pk):
        room = self.get_object(pk)
        serializer = roomSerializer(room)
        return Response(serializer.data)

class ApiHome(APIView):
    def get(self, request):
        info = ['GET/ GET rooms/ GET rooms/<str:pk>/']
        return Response(info)