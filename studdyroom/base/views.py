from email import message
from pydoc_data.topics import topics
import queue
import re
from unicodedata import name
from venv import create
from django.shortcuts import render, redirect
from django.db.models import Q

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.http import HttpResponse
from django.views import View
from .models import Room, Topic, Message, User
from .forms import RoomForm, UserForm, MyUserCreationForm
# Create your views here.


class LoginPage(View):
    
    def __init__(self):
        self.page='login'
        self.context = {'page': self.page}

    def set_params_from_post(self, request):
        self.email = request.POST.get('email').lower()
        self.password = request.POST.get('password')
        self.user = authenticate(request, email=self.email, password=self.password)
        return self.user

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        return render(request, 'base/login_register.html', self.context)

    

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        self.set_params_from_post(request)
        try:
            User.objects.get(email=self.email)
        except:
            messages.error(request, 'user does not exist')
        if self.user:
            login(request, self.user)
            return redirect('home')
        else:
            messages.error(request, 'user name or password is incorrect')
        return render(request, 'base/login_register.html', self.context)

    


def LogoutUser(request):
    
    logout(request)
    return redirect('home')

def registerPage(request):
    page='Register'
    
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
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
    topics = Topic.objects.all()[:4]
    room_count = rooms.count()
    room_messages =  Message.objects.filter(
        Q(room__name__icontains=queue))

    context = {
        'rooms': rooms, 'topics': topics,
        'room_count': room_count, 'room_messages': room_messages}
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


def UserProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {
        'user': user,
        'rooms': rooms,
        'room_messages': room_messages,
        'topics': topics
        }
    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )
        return redirect('home')

    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if  request.user != room.host:
        return HttpResponse('you can`t not edit this room')
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
    
    context = {'form': form, 'topics': topics, 'room': room}
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

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    context = {'form': form}
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)
    return render(request, 'base/update_user.html', context)


def topicsPage(request):
    queue = request.GET.get('q', '')
    topics = Topic.objects.filter(name__icontains=queue)
    context = {'topics': topics}
    return render(request, 'base/topics.html', context)


def activities(request):
    queue = request.GET.get('q', '')
    room_messages =  Message.objects.filter(
        Q(room__name__icontains=queue))
    context = {'room_messages': room_messages}
    return render(request, 'base/activity.html', context=context)