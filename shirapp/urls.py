from django.urls import path
from . views import list_view, home_view, detail_view

urlpatterns = [
    path('', home_view, name="home"),
    path('lists/', list_view, name = "lists"),
    path('list/<int:id>/', detail_view, name = "detail"),
]