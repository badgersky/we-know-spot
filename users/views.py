from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from users.forms import LoginForm


class LoginView(View):

    def get(self, request):
        form = LoginForm()
        return render(request, 'users/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)

        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password')
            )
            if user is not None:
                login(request, user)
                return redirect(reverse('home:home'))

        return render(request, 'users/login.html', {'form': form})
