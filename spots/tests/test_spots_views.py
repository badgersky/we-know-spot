from django.urls import reverse


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
