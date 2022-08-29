from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q

from django.contrib.auth.views import LoginView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView, RedirectView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Room, Topic, Message
from .forms import RoomForm


class UserLoginView(LoginView):
    template_name = "base/login_register.html"
    next_page = '/'
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'login'
        return context


class UserLogoutView(RedirectView):
    pattern_name = 'home'

    def get_redirect_url(self, *args, **kwargs):
        logout(self.request)
        return super().get_redirect_url(*args, **kwargs)


class UserRegistrationView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'base/login_register.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'register'
        return context


class HomeView(TemplateView):
    template_name = 'base/home.html'

    def get_context_data(self, **kwargs):
        q = self.request.GET.get('q') if self.request.GET.get('q') is not None else ''
        rooms = Room.objects.filter(
            Q(topic__name__icontains=q) |
            Q(name__icontains=q) |
            Q(description__icontains=q)
        )
        context = super().get_context_data(**kwargs)
        context['rooms'] = rooms
        context['topics'] = Topic.objects.all()
        context['room_count'] = rooms.count()
        return context


#TODO: Add Message Send Functionality
class RoomReview(DetailView):
    model = Room
    template_name = 'base/room.html'
    context_object_name = 'room'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['room_messages'] = self.object.message_set.all().order_by('-created')
        context['participants'] = self.object.participants.all()
        return context


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()

    if(request.method == 'POST'):
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room, 'room_messages': room_messages, 'participants': participants}
    return render(request, 'base/room.html', context)


class CreateRoomView(LoginRequiredMixin, CreateView):
    model = Room
    form_class = RoomForm
    template_name = 'base/room_form.html'
    success_url = '/'
    login_url = '/login'


#TODO: Only Room host can update room - restrict
class UpdateRoomView(LoginRequiredMixin, UpdateView):
    model = Room
    form_class = RoomForm
    template_name = 'base/room_form.html'
    success_url = '/'
    login_url = '/login'


#TODO: Only Room host can updzate room - restrict
class DeleteRoomView(LoginRequiredMixin, DeleteView):
    model = Room
    template_name = 'base/delete.html'
    success_url = '/'
    login_url = '/login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['obj'] = self.get_object()
        return context
