from django.db.models import Count
from django.views.generic import DetailView, ListView

from .models import Project, ProjectImage


def is_htmx_partial(request):
    """
    True for HTMX requests that want a fragment, not a full page.

    History-restore requests (Back button after a cache miss) need the full page.
    """
    return (
        request.headers.get("HX-Request") == "true"
        and request.headers.get("HX-History-Restore-Request") != "true"
    )


class ProjectListView(ListView):
    template_name = "projects/project_list.html"
    partial_template_name = "projects/partials/project_results.html"
    context_object_name = "projects"

    def get_active_category(self):
        category = self.request.GET.get("category", "")
        return category if category in Project.Category.values else ""
    

    def get_queryset(self):
        projects = Project.objects.published().select_related("service")
        category = self.get_active_category()
        if category:
            projects = projects.filter(category=category)
        return projects


    def get_template_names(self):
        if is_htmx_partial(self.request):
            return [self.partial_template_name]
        return [self.template_name]
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        active = self.get_active_category()

        # One grouped query: {"kitchen": 2, "extension": 2, ...}
        # .order_by() clears the model's default ordering, which could otherwise break the GROUP BY.
        counts = dict(
            Project.objects.published()
            .order_by()
            .values_list("category")
            .annotate(total=Count("id"))
        )
        categories = [{"key": "", "label": "All", "count": sum(counts.values()), "active": active == ""}]
        categories += [
            {"key": value, "label": label, "count": counts.get(value, 0), "active": active == value}
            for value, label in Project.Category.choices
        ]

        shown = len(context["projects"])
        active_label = Project.Category(active).label if active else ""
        if active:
            summary = f"Showing {shown} {active_label.lower()} project{'' if shown == 1 else 's'}"
        else:
            summary = f"Showing all {shown} project{'' if shown == 1 else 's'}"

        context.update(
            categories=categories,
            active_category=active,
            active_label=active_label,
            results_summary=summary,
            is_htmx=is_htmx_partial(self.request),
        )
        return context
    

class ProjectDetailView(DetailView):
    template_name = "projects/project_detail.html"
    context_object_name = "project"

    def get_queryset(self):
        # Drafts 404 because they're never in this queryset.
        return Project.objects.published().select_related("service").prefetch_related("images")
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.object

        images = [image for image in project.images.all() if image.image]
        before = next((i for i in images if i.kind == ProjectImage.Kind.BEFORE), None)
        after = next((i for i in images if i.kind == ProjectImage.Kind.AFTER), None)
        show_comparison = bool(before and after)

        gallery = [i for i in images if i.kind == ProjectImage.Kind.GALLERY]
        if not show_comparison:
            # A lone before and after photo still deserves a place on the page.
            gallery += [i for i in (before, after) if i]

        published_ids = list(Project.objects.published().values_list("pk", flat=True))
        next_project = None
        if len(published_ids) > 1:
            position = published_ids.index(project.pk)
            next_pk = published_ids[(position + 1) % len(published_ids)]
            next_project = Project.objects.only("title", "slug").get(pk=next_pk)

        context.update(
            before_image=before if show_comparison else None,
            after_image=after if show_comparison else None,
            gallery_images=gallery,
            next_project=next_project,
        )
        return context
