import queue
import re
from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse
from .models import Room, Topic
from .forms import RoomForm
# Create your views here.




rooms = [
    {'id': 1, 'name': 'lets learn python'},
    {'id': 2, 'name': 'lets learn django'},
    {'id': 3, 'name': 'lets learn flask'},
]

# funtion to render the index page
def home(request):
    queue = request.GET.get('q', '')
    rooms = Room.objects.filter(
        Q(topic__name__icontains=queue) |
        Q(name__icontains=queue) |
        Q(description__icontains=queue)
        )
    topics = Topic.objects.all()
    room_count = rooms.count()
    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count}
    return render(request, 'base/home.html', context)

def room(request, pk):
    context = {}
    for room in rooms:
        if room['id'] == int(pk):
            context = {'room': room}
    return render(request, 'base/room.html', context)

def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)


def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context = {'form': form}
    return render(request, 'base/room_form.html', context)

def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})