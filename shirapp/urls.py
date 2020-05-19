from django.urls import path
from . views import list_view, home_view, detail_view, create_view

urlpatterns = [
    path('', home_view, name="home"),
    path('lists/', list_view, name = "lists"),
    path('list/<int:tweet_id>/', detail_view, name="detail"),
    path('create/', create_view, name = "create"), 
]
