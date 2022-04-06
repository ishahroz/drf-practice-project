from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name="login"),
    path('logout/', views.UserLogoutView.as_view(), name="logout"),
    path('register/', views.UserRegistrationView.as_view(), name="register"),

    path('', views.HomeView.as_view(), name="home"),
    
    path('room/<str:pk>/', views.RoomReview.as_view(), name="room"),
    path('create-room/', views.CreateRoomView.as_view(), name="create-room"),
    path('update-room/<str:pk>/', views.UpdateRoomView.as_view(), name="update-room"),
    path('delete-room/<str:pk>/', views.DeleteRoomView.as_view(), name="delete-room"),
]