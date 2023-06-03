import pytest


@pytest.fixture
def user(django_user_model):
    """user instance"""

    user = django_user_model.objects.create_user(
        username='test_user',
        password='test_pass'
    )

    return user
