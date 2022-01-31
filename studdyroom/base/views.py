from email import message
import queue
import re
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from django.http import HttpResponse
from .models import Room, Topic, Message
from .forms import RoomForm
# Create your views here.




rooms = [
    {'id': 1, 'name': 'lets learn python'},
    {'id': 2, 'name': 'lets learn django'},
    {'id': 3, 'name': 'lets learn flask'},
]

def loginPage(request):
    
    page='login'
    context = {'page': page}
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'user does not exist')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'user name or password is incorrect')
    return render(request, 'base/login_register.html', context)


def LogoutUser(request):
    
    logout(request)
    return redirect('home')

def registerPage(request):
    page='Register'
    
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Something went wrong')
    context = {'page': page, 'form': form}
    return render(request, 'base/login_register.html', context)

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
    room = Room.objects.get(id=pk)
    participants = room.participants.all()
    room_messages = room.message_set.all().order_by('-created')
    if request.method == 'POST':
        message = request.POST.get('body')
        if message:
            Message.objects.create(
                user=request.user,
                room=room,
                body=message
            )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
        
    context = {
        'room': room,
        'room_messages': room_messages,
        'participants': participants
        }
    return render(request, 'base/room.html', context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if  request.user != room.host:
        return HttpResponse('you can`t not edit this room')
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context = {'form': form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if  request.user != room.host:
        return HttpResponse('you can`t not deleted this room')
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})

@login_required(login_url='login')
def deleteMessage(request, pk):
    messages = Message.objects.get(id=pk)
    if  request.user != messages.user:
        return HttpResponse('you can`t not deleted this messages')
    if request.method == 'POST':
        messages.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': messages})