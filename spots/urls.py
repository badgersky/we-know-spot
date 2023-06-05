from django.urls import path

from . import views

app_name = 'spots'

urlpatterns = [
    path('create/', views.CreateSpotView.as_view(), name='create'),
    path('list/', views.ListSpotsView.as_view(), name='list'),
]
