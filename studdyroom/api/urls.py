from django.urls import  path
from . import views

urlpatterns = [
    path('', views.ApiHome.as_view(), name='index'),
    path('rooms', views.roomsView.as_view(), name='api-rooms'),
    path('rooms/<str:pk>/', views.roomView.as_view(), name='api-room')
    ]