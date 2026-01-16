# Create your views here.
from collections import defaultdict
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, login
from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import PermissionDenied
from .forms import CardForm, CommentForm, AttachmentForm, UserCreateForm, AdminSetupForm
from .models import Card, Attachment


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
        pk=pk,
    )

    comment_form = CommentForm()
    attachment_form = AttachmentForm()

    if request.method == "POST":
        # add comment
        if "add_comment" in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.card = card
                comment.created_by = request.user
                comment.save()
                return redirect("card_detail", pk=card.pk)

        # add attachment
        elif "add_attachment" in request.POST:
            attachment_form = AttachmentForm(request.POST, request.FILES)
            if attachment_form.is_valid():
                att = attachment_form.save(commit=False)
                att.card = card
                att.uploaded_by = request.user
                att.save()
                return redirect("card_detail", pk=card.pk)

    comments = card.comments.select_related("created_by").order_by("created_at")
    attachments = card.attachments.select_related("uploaded_by").order_by("-uploaded_at")

    return render(
        request,
        "board/card_detail.html",
        {
            "card": card,
            "comments": comments,
            "attachments": attachments,
            "comment_form": comment_form,
            "attachment_form": attachment_form,
        },
    )


@login_required
def card_create_view(request):
    if request.method == "POST":
        form = CardForm(request.POST)
        if form.is_valid():
            card = form.save(commit=False)

            card.reporter = request.user
            card.created_by = request.user
            card.last_updated_by = request.user
            card.save()

            for f in request.FILES.getlist("files"):
                Attachment.objects.create(
                    card=card,
                    file=f,
                    uploaded_by=request.user,
                )

            return redirect("card_detail", pk=card.pk)
    else:
        form = CardForm()

    return render(request, "board/card_form.html", {"form": form})


@login_required
def card_edit_view(request, pk: int):
    card = get_object_or_404(Card, pk=pk)

    if request.method == "POST":
        form = CardForm(request.POST, instance=card)
        if form.is_valid():
            card = form.save(commit=False)
            card.last_updated_by = request.user
            card.save()
            return redirect("card_detail", pk=card.pk)
    else:
        form = CardForm(instance=card)

    return render(request, "board/card_form.html", {"form": form, "card": card})

User = get_user_model()

@login_required
def user_list_view(request):
    if not request.user.is_staff:
        raise PermissionDenied

    users = User.objects.order_by("id")
    return render(request, "board/user_list.html", {"users": users})


@login_required
def user_toggle_active_view(request, pk: int):
    if not request.user.is_staff:
        raise PermissionDenied
    
    if request.method != "POST":
        raise PermissionDenied

    u = get_object_or_404(User, pk=pk)

    if u.pk == request.user.pk:
        return redirect("users_list")

    u.is_active = not u.is_active
    u.save(update_fields=["is_active"])

    return redirect("users_list")


@login_required
def user_create_view(request):
    if not request.user.is_staff:
        raise PermissionDenied

    if request.method == "POST":
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = False
            user.is_superuser = False
            user.is_active = True
            user.save()
            return redirect("users_list")
    else:
        form = UserCreateForm()

    return render(request, "board/user_form.html", {"form": form})


def setup_admin_view(request):
    if User.objects.filter(is_superuser=True).exists():
        return redirect("board")

    if request.method == "POST":
        form = AdminSetupForm(request.POST)
        if form.is_valid():
            admin_user, _ = User.objects.get_or_create(username="admin")
            admin_user.is_staff = True
            admin_user.is_superuser = True
            admin_user.is_active = True
            admin_user.set_password(form.cleaned_data["password1"])
            admin_user.save() 

            login(request, admin_user)
            return redirect("board")
    else:
        form = AdminSetupForm()
    
    return render(request, "board/setup_admin.html", {"form": form})

