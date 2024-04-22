from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.apps import apps

from .forms import SignUpForm

# Create your views here.

# class LoginView(FormView)
# GET - отдает форму с запросом логина и пароля
# POST - генерирует сессию: отдавая ее ползователю


class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('main_page')
    template_name = 'accounts/signup.html'


class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_field_name = 'next' # default
    extra_context = {}
    authentication_form = AuthenticationForm # default


# LogoutView(TemplateView)
class UserLogoutView(LogoutView):
    template_name = 'accounts/logout.html'
    next_page = reverse_lazy('main_page')
    redirect_field_name = 'next'
    extra_context = {}