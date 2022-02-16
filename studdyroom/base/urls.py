from django.urls import  path
from . import views

urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('login/', views.LoginPage.as_view(), name='login'),
    path('register/', views.RegisterPage.as_view(), name='register'),
    path('logout/', views.LogoutUser, name='logout'),
    path('room/<str:pk>/', views.RoomView.as_view(), name='room'),
    path('profile/<str:pk>/', views.UserProfile.as_view(), name='user-profile'),
    path('create-room/', views.CreateRoom.as_view(), name='create-room'),
    path('update-room/<str:pk>/', views.updateRoom, name='update-room'),
    path('delete-room/<str:pk>/', views.deleteRoom, name='delete-room'),
    path('delete-message/<str:pk>/', views.deleteMessage, name='delete-message'),
    path('update-user/', views.updateUser, name='update-user'), 
    path('topics/', views.topicsPage, name='topics'),
    path('activities/', views.activities, name='activities')
]