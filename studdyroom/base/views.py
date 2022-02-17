from pydoc_data.topics import topics
from django.shortcuts import render, redirect
from django.db.models import Q

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.decorators import login_required
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
        self.user = User.objects.filter(email=self.email).first()
        if not self.user or not self.user.check_password(self.password):
            self.user = None

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        return render(request, 'base/login_register.html', self.context)

    

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        self.set_params_from_post(request)
        
        if self.user:
            login(request, self.user)
            return redirect('home')
        else:
            messages.error(request, 'user name or password is incorrect')
        return render(request, 'base/login_register.html', self.context)

    


def LogoutUser(request):
    
    logout(request)
    return redirect('home')

class RegisterPage(View):
    """"""
    def __init__(self):
        self.page='Register'
        self.form = MyUserCreationForm()
        self.context = {'page': self.page, 'form': self.form}
    
    def get(self, request):
        return render(request, 'base/login_register.html', self.context)

    def post(self, request):
        if self.form.is_valid():
            user = self.form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Something went wrong')
        return render(request, 'base/login_register.html', self.context)

class HomePage(View):
    def get(self, request):
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

class RoomView(View):
    def get(self, request, pk):
        context = {}
        room = Room.objects.get(id=pk)
        participants = room.participants.all()
        room_messages = room.message_set.all().order_by('-created')
        context = {
            'room': room,
            'room_messages': room_messages,
            'participants': participants
            }
        return render(request, 'base/room.html', context)
    
    def post(self, request, pk):
        message = request.POST.get('body')
        room = Room.objects.get(id=pk)
        if message:
            Message.objects.create(
                user=request.user,
                room=room,
                body=message
            )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)


class UserProfile(View):
    def get(self, request, pk):
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

class CreateRoom(LoginRequiredMixin, View):

    def __init__(self):
        self.topics = Topic.objects.all()
        login_url = '/login/'
        redirect_field_name = 'redirect_to'
    
    def get(self, request):
        form = RoomForm()
        context = {'form': form, 'topics': self.topics}
        return render(request, 'base/room_form.html', context)
   
    #
    def post(self, request):
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.topic = Topic.objects.get(id=request.POST.get('topic'))
            room.save()
            return redirect('room', pk=room.id)
        else:
            messages.error(request, 'Something went wrong')
        context = {'form': form, 'topics': self.topics}
        return render(request, 'base/room_form.html', context)




class UpdateRoom(LoginRequiredMixin, View):
    def __init__(self):
        login_url = '/login/'
        redirect_field_name = 'redirect_to'
    
    def get(self, request, pk):
        if  request.user != room.host:
            return HttpResponse('you can`t not edit this room')
        room = Room.objects.get(id=pk)
        form = RoomForm(instance=room)
        topics = Topic.objects.all()
        context = {'form': form, 'topics': topics, 'room': room}
        return render(request, 'base/room_form.html', context)

    def post(self, request, pk):
        room = Room.objects.get(id=pk)
        if  request.user != room.host:
            return HttpResponse('you can`t not edit this room')
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')


class DeleteRoom(LoginRequiredMixin, View):
    def __init__(self):
        login_url = '/login/'
        redirect_field_name = 'redirect_to'
    
    def get(self, request, pk):
        room = Room.objects.get(id=pk)
        if  request.user != room.host:
            return HttpResponse('you can`t not deleted this room')
    
    def post(self, request, pk):
        room = Room.objects.get(id=pk)
        room.delete()
        return redirect('home')


class DeleteMessage(LoginRequiredMixin, View):
    
    def __init__(self):
        login_url = '/login/'
        redirect_field_name = 'redirect_to'
    
    def get(self, request, pk):
        messages = Message.objects.get(id=pk)
        if  request.user != messages.user:
            return HttpResponse('you can`t not deleted this messages')
        return render(request, 'base/delete.html', {'obj': messages})

    def post(self, request, pk):
        if  request.user != messages.user:
            return HttpResponse('you can`t not deleted this messages')
        messages = Message.objects.get(id=pk)
        messages.delete()
        return redirect('home')
    

class UpdateUser(LoginRequiredMixin, View):
    def __init__(self):
        login_url = '/login/'
        redirect_field_name = 'redirect_to'
    
    def get(self, request):
        user = request.user
        form = UserForm(instance=user)
        context = {'form': form}
        return render(request, 'base/update_user.html', context)

    def post(self, request):
        user = request.user
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)
        context = {'form': form}
        return render(request, 'base/update_user.html', context)


class TopicsPage(View):
    def get(self, request, q):
        queue = q
        topics = Topic.objects.filter(name__icontains=queue)
        context = {'topics': topics}
        return render(request, 'base/topics.html', context)


class Activities(View):
    def get(self, request, q):
        queue = q
        room_messages =  Message.objects.filter(
            Q(room__name__icontains=queue))
        context = {'room_messages': room_messages}
        return render(request, 'base/activity.html', context=context)