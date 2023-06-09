from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.views import View

from spots.models import Spot


class HomeView(View):

    def get(self, request):
        spots_num = Spot.objects.count()
        user_num = get_user_model().objects.count()
        return render(request, 'home/home.html', {'spots_num': spots_num, 'user_num': user_num})
