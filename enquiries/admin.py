from django.contrib import admin
from django.utils.html import format_html_join

from .models import Enquiry, EnquiryNote


class EnquiryNoteInline(admin.StackedInline):
    model = EnquiryNote
    extra = 1
    fields = ["body", "written_by", "created_at"]
    readonly_fields = ["written_by", "created_at"]

    @admin.display(description="Written by")
    def written_by(self, obj):
        return obj.author_display_name if obj.pk else "You (on save)"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("author")


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "postcode", "service", "status", "created_at"]
    list_filter = ["status", "service", "created_at"]
    list_select_related = ["service"]
    search_fields = ["name", "email", "postcode"]
    date_hierarchy = "created_at"
    inlines = [EnquiryNoteInline]

    readonly_fields = [
        "name", "email", "phone", "service", "postcode",
        "project_description", "preferred_contact_method",
        "status_history", "created_at", "updated_at",
    ]
    fieldsets = [
        ("Customer", {"fields": ["name", "email", "phone", "preferred_contact_method", "postcode"]}),
        ("Request", {"fields": ["service", "project_description"]}),
        ("Progress", {"fields": ["status", "status_history"]}),
        ("Record", {"fields": ["created_at", "updated_at"], "classes": ["collapse"]}),
    ]

    def has_add_permission(self, request):
        # Enquiries only ever come from the public quote form.
        return False

    @admin.display(description="Status history")
    def status_history(self, obj):
        changes = obj.status_changes.select_related("changed_by")
        if not changes:
            return "No changes yet."
        return format_html_join(
            "",
            "<div>{} → {} · {} · {}</div>",
            (
                (
                    c.get_from_status_display(),
                    c.get_to_status_display(),
                    c.changed_by_display_name,
                    c.created_at.strftime("%d %b %Y, %H:%M"),
                )
                for c in changes
            ),
        )

    def save_model(self, request, obj, form, change):
        # Route status changes through change_status() so history is recorded.
        if change and "status" in form.changed_data:
            new_status = obj.status
            obj.status = form.initial["status"]
            obj.change_status(new_status, request.user)
        else:
            super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        # Sign new notes with the logged-in user.
        notes = formset.save(commit=False)
        for note in notes:
            if note.author_id is None:
                note.author = request.user
            note.save()
        for deleted in formset.deleted_objects:
            deleted.delete()