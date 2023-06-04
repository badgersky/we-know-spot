from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

from spots.forms import CreateSpotForm


class CreateSpotView(LoginRequiredMixin, CreateView):
    """view for adding spot to database"""

    login_url = reverse_lazy('users:login')
    form_class = CreateSpotForm
    template_name = 'spots/create-spot.html'
    success_url = reverse_lazy('home:home')
    context_object_name = 'form'

    def form_valid(self, form):
        spot = form.save(commit=False)
        spot.user = self.request.user
        return spot

    def get_login_url(self):
        messages.add_message(
            self.request,
            messages.WARNING,
            f'Login in order to create spot',
        )
        return super().get_login_url()
    