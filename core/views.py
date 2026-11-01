from django.views.generic import TemplateView

from projects.models import Project
from services.models import Service

PROCESS_STEPS = [
    ("Visit", "We come and see the house, listen, and take measurements."),
    ("Quote", "An itemised quote and programme, with no hidden extras."),
    ("Build", "One project lead and weekly updates until handover."),
    ("Care", "Snagging, aftercare and an optional maintenance plan."),
]

SERVICE_AREAS = [
    "Clifton", "Redland", "Bath", "Keynsham",
    "Portishead", "Clevedon", "Chew Valley", "Bradford-on-Avon",
]

TEAM = [
    ("Alex Morgan", "AM", "Founder · Lead carpenter", "Started Northstar after years of watching good homes get rushed renovations."),
    ("Sarah Jones", "SJ", "Project lead", "Your main point of contact, from the first visit to the final handover."),
    ("Priya Desai", "PD", "Designer", "Turns rough ideas into layouts, drawings and finishes that suit how you live."),
    ("Owen Hughes", "OH", "Site manager", "Keeps every trade on programme and every site tidy, safe and secure."),
]
class HomeView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        featured = list(Project.objects.featured().select_related("service")[:3])
        context.update(
            services=Service.objects.active(),
            featured_projects=featured,
            hero_project=featured[0] if featured else None,
            process_steps=PROCESS_STEPS,
            service_areas=SERVICE_AREAS,
        )
        return context
    

class AboutView(TemplateView):
    template_name = "core/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["team"] = TEAM
        return context


class PrivacyView(TemplateView):
    template_name = "core/privacy.html"
