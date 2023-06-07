from django.contrib.auth.mixins import AccessMixin


class OwnerRequiredMixin(AccessMixin):
    """Verify that the current user is admin or spot creator"""

    def dispatch(self, request, *args, **kwargs):
        spot = self.get_queryset().get(pk=kwargs.get('pk'))
        if request.user != spot.user or not request.user.is_superuser:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
