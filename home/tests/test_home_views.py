from django.urls import reverse


def test_home_page(client, db, django_user_model):
    url = reverse('home:home')

    response = client.get(url)

    assert response.status_code == 200
    assert 'About' in response.content.decode('utf-8')
    assert str(django_user_model.objects.count()) in response.content.decode('utf-8')
    