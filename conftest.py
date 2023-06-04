import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from spots.models import Province, Tag


@pytest.fixture
def user(django_user_model):
    """user instance"""

    user = django_user_model.objects.create_user(
        username='test_user',
        password='test_pass'
    )

    return user


@pytest.fixture
def province():
    """province instance"""

    province = Province.objects.create(
        province_name='test_province',
        main_city='test_city'
    )

    return province


@pytest.fixture
def tags():
    """tags instances"""

    for i in range(1, 6):
        tag = Tag(tag_name=f'tag{i}')
        yield tag


@pytest.fixture
def photo():
    """photo object"""

    photo = SimpleUploadedFile('test.jpg', b'image')
    return photo
