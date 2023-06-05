from django.urls import reverse

from spots.models import Spot


def test_create_spot_view_get(client, user):
    url = reverse('spots:create')
    client.force_login(user)

    response = client.get(url)

    assert response.status_code == 200
    assert 'Create Spot' in response.content.decode('utf-8')


def test_create_spot_view_no_permission(client):
    url = reverse('spots:create')

    redirect = client.get(url)
    response = client.get(redirect.url)

    assert redirect.status_code == 302
    assert response.status_code == 200
    assert 'Login' in response.content.decode('utf-8')


def test_create_spot_view_post(client, user, province, tags, photo):
    url = reverse('spots:create')
    client.force_login(user)
    print([str(tag.pk) for tag in tags])
    data = {
        'name': 'test-spot',
        'province': str(province.pk),
        'longitude': 19.489387,
        'latitude': 49.789646,
        'tags': [str(tag.pk) for tag in tags],
        'photo': photo
    }
    num_of_spots = Spot.objects.count()

    redirect = client.post(url, data)
    response = client.get(redirect.url)
    num_of_spots_after = Spot.objects.count()

    assert redirect.status_code == 302
    assert response.status_code == 200
    assert num_of_spots == num_of_spots_after - 1
    assert 'Spot created successfully' in response.content.decode('utf-8')


def test_create_spot_view_invalid_form(client, user, province, tags):
    url = reverse('spots:create')
    client.force_login(user)
    data = {
        'name': 'test-spot',
        'province': str(province.pk),
        'longitude': 19.489387,
        'latitude': 49.789646,
        'tags': [str(tag.pk) for tag in tags],
        'photo': '',
    }
    num_of_spots = Spot.objects.count()

    response = client.post(url, data)
    num_of_spots_after = Spot.objects.count()

    assert response.status_code == 200
    assert num_of_spots == num_of_spots_after
    assert 'Create Spot' in response.content.decode('utf-8')
