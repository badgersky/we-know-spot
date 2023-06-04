from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import CreateView

from spots.forms import CreateSpotForm


class CreateSpotView(LoginRequiredMixin, CreateView):
    """view for adding spot to database"""

    login_url = reverse('users:login')
    form_class = CreateSpotForm()
    template_name = 'spots/create-spot.html'
    success_url = reverse('home:home')
    context_object_name = 'form'

    def form_valid(self, form):
        spot = form.save(commit=False)
        spot.user = self.request.user
        return spot
