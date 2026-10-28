from django.views.generic import DeleteView, ListView

from .models import Service

class ServiceListView(ListView):
    template_name = "services/service_list.html"
    context_object_name = "services"

    def get_queryset(self):
        return Service.objects.active()
    

class ServiceDetailView(DeleteView):
    template_name = "services/service_detail.html"
    context_object_name = "service"

    def get_queryset(self):
        # Inactive services 404 because they're never in this queryset.
        return Service.objects.active()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service = self.object
        active_ids = list(Service.objects.active().values_list("pk", flat=True))
        context.update(
            number=active_ids.index(service.pk) + 1,
            related_projects=service.projects.published()[:2],
            other_services=Service.objects.active().exclude(pk=service.pk),
        )
        return context
