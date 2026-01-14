from django.contrib import admin
from .models import Card, Comment, Attachment

# Register your models here.

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "status", "priority", "assignee", "reporter", "updated_at")
    list_filter = ("status", "priority")
    search_fields = ("name", "description")
    autocomplete_fields = ("assignee", "reporter", "created_by", "last_updated_by")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "card", "created_by", "created_at")
    search_fields = ("text",)
    autocomplete_fields = ("card", "created_by")


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ("id", "card", "file", "uploaded_by", "uploaded_at")
    autocomplete_fields = ("card", "uploaded_by")
