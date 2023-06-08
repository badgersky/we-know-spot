from io import BytesIO

import pytest
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile

from spots.models import Province, Tag, Spot


@pytest.fixture
def user(django_user_model):
    """user instance"""

    user = django_user_model.objects.create_user(
        username='test_user',
        password='test_pass'
    )

    return user


@pytest.fixture
def user2(django_user_model):
    """second user instance"""

    user2 = django_user_model.objects.create_user(
        username='test_user2',
        password='test_pass2',
    )

    return user2


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

    tags = []
    for i in range(1, 4):
        new_tag = Tag.objects.create(tag_name=f'test_tag{i}')
        new_tag.save()
        tags.append(new_tag)

    return tags


@pytest.fixture
def photo():
    """temporary photo object"""

    bts = BytesIO()
    img = Image.new("RGB", (100, 100))
    img.save(bts, 'jpeg')
    return SimpleUploadedFile("test.jpg", bts.getvalue())


@pytest.fixture
def spots(province, tags, photo, user):
    """temporary spots"""

    spots = []
    for i in range(1, 6):
        new_spot = Spot.objects.create(
            name=f'spot{i}',
            province=province,
            longitude=20.000000,
            latitude=50.000000,
            photo=photo,
            user=user
        )
        new_spot.tags.set(tags)
        new_spot.save()
        spots.append(new_spot)

    return spots
