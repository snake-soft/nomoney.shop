from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic import View
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls.base import reverse
from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from user.models import User
from .models import Chat
from .forms import ChatMessageForm

# chat/views.py

def index(request):
    return render(request, 'chat/index.html', {})

def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })


class ChatListView(LoginRequiredMixin, ListView):
    model = Chat
    context_object_name = 'chats'

    def get_queryset(self):
        return self.request.user.chats

    def get_context_data(self, **kwargs):
        context = ListView.get_context_data(self, **kwargs)
        context['lobby'] = Chat.get_lobby()
        return context


class ChatDetailView(LoginRequiredMixin, DetailView):
    model = Chat
    context_object_name = 'chat'

    def get_context_data(self, **kwargs):
        kwargs['form'] = ChatMessageForm(self.request.POST)
        return DetailView.get_context_data(self, **kwargs)


class ChatUserDetailView(LoginRequiredMixin, DetailView):
    model = Chat
    context_object_name = 'chat'

    def get_object(self, queryset=None):
        user_pk = self.request.resolver_match.kwargs.get('user_pk')
        user = User.objects.get(pk=user_pk)
        return Chat.by_users(self.request.user, user)


class ChatCreateView(LoginRequiredMixin, CreateView):
    model = Chat
    fields = ['users']

    def get_form(self, form_class=None):
        form = CreateView.get_form(self, form_class=form_class)
        form.fields['users'].widget.attrs['class'] = 'chosen-select'
        form.fields['users'].widget.attrs['data-placeholder'] = \
            'Benutzer auswählen ...'
        form.fields['users'].queryset = form.fields['users'].queryset.exclude(
            pk=self.request.user.pk)
        return form

    def form_valid(self, form):
        chat = Chat.by_users(*form.cleaned_data['users'], self.request.user, create=True)
        return HttpResponseRedirect(reverse('chat_detail', args=(chat.pk,)))


class ChatNewMessageView(LoginRequiredMixin, CreateView):
    form_class = ChatMessageForm

    def form_valid(self, form):
        chat_pk = self.request.resolver_match.kwargs.get('pk')
        form.instance.chat = Chat.objects.get(pk=chat_pk)
        form.instance.creator = self.request.user
        return CreateView.form_valid(self, form)

    def get_success_url(self):
        return reverse('chat_detail', args=(
            self.request.resolver_match.kwargs.get('pk'),
            ))


class ChatAjaxStatusView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):  # future?
        import pdb; pdb.set_trace()  # <---------
        return JsonResponse({'foo': 'bar'})


class ChatAjaxView(LoginRequiredMixin, DetailView):
    model = Chat
    template_name = 'chat/solo/chat_messages_ajax.html'
