from django.contrib import admin

from core.admin import image_thumbnail
from .models import Project, ProjectImage

class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1
    fields = ["preview", "image", "alt_text", "kind", "caption", "display_order"]
    readonly_fields = ["preview"]

    @admin.display(description="Preview")
    def preview(self, obj):
        return image_thumbnail(obj.image)
    

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = [
        "title", "thumbnail", "category", "service",
        "is_published", "is_featured", "completed_at",
    ]
    list_editable = ["is_published", "is_featured"]
    list_filter = ["is_published", "is_featured", "category", "service"]
    list_select_related = ["service"]
    search_fields = ["title", "summary", "location"]
    prepopulated_fields = {"slug": ["title"]}
    date_hierarchy = "completed_at"
    readonly_fields = ["featured_image_preview", "created_at", "updated_at"]
    inlines = [ProjectImageInline]

    fieldsets = [
        (None, {"fields": ["title", "slug", "category", "service", "location", "completed_at"]}),
        ("Content", {"fields": ["summary", "description"]}),
        ("Featured image", {"fields": ["featured_image", "featured_image_preview", "featured_image_alt"]}),
        ("Visibility", {"fields": ["is_published", "is_featured"]}),
        ("Record", {"fields": ["created_at", "updated_at"], "classes": ["collapse"]}),
    ]

    @admin.display(description="Image")
    def thumbnail(self, obj):
        return image_thumbnail(obj.featured_image, height=40)

    @admin.display(description="Preview")
    def featured_image_preview(self, obj):
        return image_thumbnail(obj.featured_image, height=160)
