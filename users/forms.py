from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):

    class Meta:
        model = get_user_model()
        fields = ('username', 'password')
        