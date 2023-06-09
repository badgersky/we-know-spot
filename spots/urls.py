from django.urls import path

from . import views

app_name = 'spots'

urlpatterns = [
    path('create/', views.CreateSpotView.as_view(), name='create'),
    path('list/', views.ListSpotsView.as_view(), name='list'),
    path('like/<pk>/', views.LikeSpot.as_view(), name='like'),
    path('search/', views.SearchSpot.as_view(), name='search'),
    path('delete/<pk>/', views.DeleteSpotView.as_view(), name='delete'),
    path('update/<pk>/', views.UpdateSpotView.as_view(), name='update'),
]
