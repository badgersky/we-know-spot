from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View

from users.forms import LoginForm, RegistrationForm


class LoginView(View):
    """view for logging in"""

    def get(self, request):
        form = LoginForm()
        return render(request, 'users/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request, request.POST)

        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password')
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(reverse('home:home'))

        return render(request, 'users/login.html', {'form': form})


class LogoutView(LoginRequiredMixin, View):
    """view for logging out"""

    login_url = reverse_lazy('users:login')

    def get(self, request):
        logout(request)
        return redirect(reverse('home:home'))


class RegisterView(View):
    """view for registering user"""

    def get(self, request):
        form = RegistrationForm()
        return render(request, 'users/register.html', {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)

        if form.is_valid():
            form.save()

            messages.add_message(
                request,
                messages.SUCCESS,
                f'Registered successfully, please login'
            )
            return redirect(reverse('users:login'))

        return render(request, 'users/register.html', {'form': form})
