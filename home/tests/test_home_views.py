from django.urls import reverse


def test_home_page(client):
    url = reverse('home:home')

    response = client.get(url)

    assert response.status_code == 200
    assert 'Home Page' in response.content.decode('utf-8')
