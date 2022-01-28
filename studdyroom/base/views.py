from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


rooms = [
    {'id': 1, 'name': 'lets learn python'},
    {'id': 2, 'name': 'lets learn django'},
    {'id': 3, 'name': 'lets learn flask'},
]

# funtion to render the index page
def home(request):
    context = {'rooms': rooms}
    return render(request, 'base/home.html', context)

def room(request, pk):
    context = {}
    for room in rooms:
        if room['id'] == int(pk):
            context = {'room': room}
    return render(request, 'base/room.html', context)