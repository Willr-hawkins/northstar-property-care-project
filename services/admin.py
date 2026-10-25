from django.contrib import admin

from core.admin import image_thumbnail
from .models import Service

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ["title", "thumbnail", "is_active", "display_order", "updated_at"]
    list_editable = ["is_active", "display_order"]
    list_filter = ["is_active"]
    search_fields = ["title", "short_description"]
    prepopulated_fields = {"slug": ["title"]}
    readonly_fields = ["image_preview", "created_at", "updated_at"]

    fieldsets = [
        (None, {"fields": ["title", "slug", "short_description", "description"]}),
        ("Image", {"fields": ["image", "image_preview", "image_alt"]}),
        ("Visibility", {"fields": ["is_active", "display_order"]}),
        ("Record", {"fields": ["created_at", "updated_at"], "classes": ["collapse"]}),
    ]

    @admin.display(description="Image")
    def thumbnail(self, obj):
        return image_thumbnail(obj.image, height=40)
    
    @admin.display(description="Preview")
    def image_preview(self, obj):
        return image_thumbnail(obj.image, height=160)
