from django.urls import path
from . import views

urlpatterns = [
    path("", views.board_view, name="board"),
    path("card/<int:pk>/", views.card_detail_view, name="card_detail"),
    path("cards/new/", views.card_create_view, name="card_create"),
]
