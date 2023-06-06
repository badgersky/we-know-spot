from django.urls import reverse

from spots.models import Spot, SpotLike


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


def test_list_spot_view_no_spots(client, db):
    url = reverse('spots:list')
    num_of_spots = Spot.objects.count()

    response = client.get(url)

    assert response.status_code == 200
    assert 'No Spots' in response.content.decode('utf-8')
    assert num_of_spots == 0


def test_list_spot_view(client, db, spots):
    url = reverse('spots:list')
    num_of_spots = Spot.objects.count()

    response = client.get(url)

    assert response.status_code == 200
    assert 'No Spots' not in response.content.decode('utf-8')
    assert num_of_spots == len(spots)
    for spot in spots:
        assert spot.name in response.content.decode('utf-8')


def test_like_spot_view(client, db, user, spots):
    url = reverse('spots:like', kwargs={'pk': spots[0].pk})
    client.force_login(user)
    likes = Spot.objects.get(pk=spots[0].pk).likes

    redirect = client.get(url)
    response = client.get(redirect.url)
    likes_after = Spot.objects.get(pk=spots[0].pk).likes

    assert redirect.status_code == 302
    assert response.status_code == 200
    assert likes == likes_after - 1
    assert SpotLike.objects.filter(user=user, spot=spots[0]).exists() is True


def test_dislike_spot_view(client, db, user, spots):
    url = reverse('spots:dislike', kwargs={'pk': spots[0].pk})
    spots[0].likes = 1
    SpotLike.objects.create(user=user, spot=spots[0])
    client.force_login(user)
    likes = Spot.objects.get(pk=spots[0].pk).likes

    redirect = client.get(url)
    response = client.get(redirect.url)
    likes_after = Spot.objects.get(pk=spots[0].pk).likes

    assert redirect.status_code == 302
    assert response.status_code == 200
    assert likes == likes_after + 1
    assert SpotLike.objects.filter(user=user, spot=spots[0]).exists() is False


def test_like_spot_view_no_permission(client, db, spots):
    url = reverse('spots:like', kwargs={'pk': spots[0].pk})
    likes = Spot.objects.get(pk=spots[0].pk).likes

    redirect = client.get(url)
    response = client.get(redirect.url)
    likes_after = Spot.objects.get(pk=spots[0].pk).likes

    assert redirect.status_code == 302
    assert response.status_code == 200
    assert likes == likes_after
    assert 'Login' in response.content.decode('utf-8')


def test_dislike_spot_view_no_permission(client, db, spots):
    url = reverse('spots:dislike', kwargs={'pk': spots[0].pk})
    likes = Spot.objects.get(pk=spots[0].pk).likes

    redirect = client.get(url)
    response = client.get(redirect.url)
    likes_after = Spot.objects.get(pk=spots[0].pk).likes

    assert redirect.status_code == 302
    assert response.status_code == 200
    assert likes == likes_after
    assert 'Login' in response.content.decode('utf-8')


