from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from spots.models import Spot


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
