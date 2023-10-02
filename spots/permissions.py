from django.contrib.auth.mixins import AccessMixin


class OwnerRequiredMixin(AccessMixin):
    """Verify that the current user is spot creator"""

    def dispatch(self, request, *args, **kwargs):
        spot = self.get_queryset().get(pk=kwargs.get('pk'))
        if request.user != spot.user:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class OwnerOrAdminRequiredMixin(AccessMixin):
    """Verify that the current user is spot creator"""

    def dispatch(self, request, *args, **kwargs):
        spot = self.get_queryset().get(pk=kwargs.get('pk'))
        if request.user != spot.user and not request.user.is_superuser():
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
