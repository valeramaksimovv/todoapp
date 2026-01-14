from django.urls import path
from . import views

urlpatterns = [
    path("", views.board_view, name="board"),
    path("card/<int:pk>/", views.card_detail_view, name="card_detail"),
    path("cards/new/", views.card_create_view, name="card_create"),
    path("card/<int:pk>/edit/", views.card_edit_view, name="card_edit"),
    path("users/", views.user_list_view, name="users_list"),
    path("user/<int:pk>/toggle/", views.user_toggle_active_view, name="user_toggle")
]
