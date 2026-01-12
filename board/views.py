# Create your views here.
from collections import defaultdict

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .forms import CardCreateForm

from .models import Card


@login_required
def board_view(request):
    cards = Card.objects.select_related("assignee", "reporter").order_by("-updated_at")

    statuses = Card.Status.choices

    grouped = defaultdict(list)
    for card in cards:
        grouped[card.status].append(card)

    columns = []
    for code, label in statuses:
        columns.append({"code": code, "label": label, "cards": grouped.get(code, [])})
        
    return render(request, "board/board.html", {"columns": columns})

@login_required
def card_detail_view(request, pk: int):
    card = get_object_or_404(
        Card.objects.select_related("assignee", "reporter", "created_by", "last_updated_by"),
        pk=pk
    )

    return render(request, "board/card_detail.html", {"card": card})

@login_required
def card_create_view(request):
    if request.method == "POST":
        form = CardCreateForm(request.POST)
        if form.is_valid():
            card = form.save(commit=False)

            card.reporter = request.user
            card.created_by = request.user
            card.last_updated_by = request.user

            card.save()
            return redirect("board")

    else:
        form = CardCreateForm()

    return render(request, "board/card_form.html", {"form": form})
