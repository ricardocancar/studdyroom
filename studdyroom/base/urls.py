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
    path('update-room/<str:pk>/', views.UpdateRoom.as_view(), name='update-room'),
    path('delete-room/<str:pk>/', views.DeleteRoom.as_view(), name='delete-room'),
    path('delete-message/<str:pk>/', views.DeleteMessage.as_view(), name='delete-message'),
    path('update-user/', views.UpdateUser.as_view(), name='update-user'), 
    path('topics/', views.TopicsPage.as_view(), name='topics'),
    path('activities/', views.Activities.as_view(), name='activities')
]