from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, ListView, DeleteView

from spots.models import Spot, SpotLike
from spots.permissions import OwnerRequiredMixin


class CreateSpotView(LoginRequiredMixin, CreateView):
    """view for adding spot to database"""

    model = Spot
    login_url = reverse_lazy('users:login')
    fields = ('name', 'province', 'longitude', 'latitude', 'tags', 'photo')
    template_name = 'spots/create-spot.html'
    success_url = reverse_lazy('home:home')

    def get_success_url(self):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            f'Spot created successfully',
        )
        return super().get_success_url()

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_login_url(self):
        messages.add_message(
            self.request,
            messages.WARNING,
            f'Login in order to create spot',
        )
        return super().get_login_url()


class ListSpotsView(ListView):
    """lists all created spots"""

    model = Spot
    template_name = 'spots/list-spots.html'
    context_object_name = 'spots'
    paginate_by = 20

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        liked_spots = []
        if self.request.user.is_authenticated:
            for spot in context['spots']:
                if SpotLike.objects.filter(user=self.request.user, spot=spot).exists():
                    liked_spots.append(spot.pk)
        context['liked_spots'] = liked_spots
        return context


class LikeSpot(LoginRequiredMixin, View):
    """view for liking spot"""
    login_url = reverse_lazy('users:login')

    def get(self, request, pk):
        spot = Spot.objects.get(pk=pk)
        if SpotLike.objects.filter(user=request.user, spot=spot).exists():
            return redirect(reverse('spots:list'))

        SpotLike.objects.create(user=request.user, spot=spot)
        spot.likes += 1
        spot.save()
        return redirect(reverse('spots:list'))


class DislikeSpot(LoginRequiredMixin, View):
    """view for disliking spot"""
    login_url = reverse_lazy('users:login')

    def get(self, request, pk):
        spot = Spot.objects.get(pk=pk)
        if SpotLike.objects.filter(user=request.user, spot=spot).exists():
            SpotLike.objects.get(user=request.user, spot=spot).delete()
            spot.likes -= 1
            spot.save()

        return redirect(reverse('spots:list'))


class SearchSpot(View):
    """view for searching spots"""

    def post(self, request):
        tag = request.POST.get('search')

        context = {
            'spots': set(Spot.objects.filter(Q(tags__tag_name=tag) | Q(province__province_name=tag) | Q(name=tag))),
            'liked_spots': [],
        }
        if request.user.is_authenticated:
            for spot in context['spots']:
                if SpotLike.objects.filter(user=self.request.user, spot=spot).exists():
                    context['liked_spots'].append(spot.pk)

        return render(request, 'spots/list-spots.html', context)


class DeleteSpotView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    """view for deleting spot"""

    model = Spot
    template_name = 'spots/delete.html'
    context_object_name = 'spot'
    success_url = reverse_lazy('spots:list')
