from django.urls import reverse


def test_login_view_get(client):
    url = reverse('users:login')

    response = client.get(url)

    assert response.status_code == 200
    assert 'Login' in response.content.decode('utf-8')


def test_login_view_post(client, user):
    url = reverse('users:login')
    data = {
        'username': 'test_user',
        'password': 'test_pass',
    }

    redirect = client.post(url, data)

    response = client.get(redirect.url)

    assert redirect.status_code == 302
    assert response.status_code == 200
    assert 'Logged in (test_user)' in response.content.decode('utf-8')


def test_logout_view(client, user):
    client.force_login(user)
    url = reverse('users:logout')

    redirect = client.get(url)

    response = client.get(redirect.url)

    assert redirect.status_code == 302
    assert response.status_code == 200
    assert 'Login' in response.content.decode('utf-8')


def test_logout_view_user_not_logged(client, user):
    url = reverse('users:logout')

    redirect = client.get(url)
    response = client.get(redirect.url)

    assert redirect.status_code == 302
    assert response.status_code == 200
    assert 'Login' in response.content.decode('utf-8')
