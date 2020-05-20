from django.urls import path
from . views import list_view, home_view, detail_view, create_view, delete_view,action_view

urlpatterns = [
    path('', home_view, name="home"),
    path('create/', create_view, name = "create"), 
    path('lists/', list_view, name = "lists"),
    path('list/<int:tweet_id>/', detail_view, name="detail"),
    path('api/list/<int:tweet_id>/delete/', delete_view, name="delete"),
    path('api/list/action',action_view, name = "action"),
]
