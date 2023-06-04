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


def test_register_view_get(client):
    url = reverse('users:register')

    response = client.get(url)

    assert response.status_code == 200
    assert 'Register' in response.content.decode('utf-8')


def test_registration_view_post(client, django_user_model):
    url = reverse('users:register')
    data = {
        'username': 'test_user',
        'password': 'test_password',
        'confirm_password': 'test_password'
    }
    num_of_users = django_user_model.objects.count()

    redirect = client.post(url, data)
    response = client.get(redirect.url)
    num_of_users_after = django_user_model.objects.count()

    assert redirect.status_code == 302
    assert response.status_code == 200
    assert 'Login' in response.content.decode('utf-8')
    assert num_of_users == num_of_users_after - 1


def test_registration_view_different_confirm_password(client, django_user_model):
    url = reverse('users:register')
    data = {
        'username': 'test_user',
        'password': 'test_password',
        'confirm_password': 'password_test'
    }
    num_of_users = django_user_model.objects.count()

    response = client.post(url, data)
    num_of_users_after = django_user_model.objects.count()

    assert response.status_code == 200
    assert 'Register' in response.content.decode('utf-8')
    assert 'Passwords don`t match' in response.content.decode('utf-8')
    assert num_of_users == num_of_users_after


def test_registration_view_user_already_exist(client, user, django_user_model):
    url = reverse('users:register')
    data = {
        'username': user.username,
        'password': 'test_password',
        'confirm_password': 'test_password',
    }
    num_of_users = django_user_model.objects.count()

    response = client.post(url, data)
    num_of_users_after = django_user_model.objects.count()

    assert response.status_code == 200
    assert 'Register' in response.content.decode('utf-8')
    assert 'Try using different username' in response.content.decode('utf-8')
    assert num_of_users == num_of_users_after


def test_registration_view_weak_password(client, django_user_model):
    url = reverse('users:register')
    data = {
        'username': 'test_user',
        'password': 'a',
        'confirm_password': 'a',
    }
    num_of_users = django_user_model.objects.count()

    response = client.post(url, data)
    num_of_users_after = django_user_model.objects.count()

    assert response.status_code == 200
    assert 'Register' in response.content.decode('utf-8')
    assert 'This password is too short. It must contain at least 8 characters.' in response.content.decode('utf-8')
    assert num_of_users == num_of_users_after
    