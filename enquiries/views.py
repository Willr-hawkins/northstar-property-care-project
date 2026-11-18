import logging

from django.db import transaction
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView, TemplateView

from services.models import Service

from .forms import QuoteForm
from .models import Enquiry
from .notifications import send_enquiry_notification

logger = logging.getLogger(__name__)

SUBMITTED_SESSION_KEY = "quote_submitted_name"


class QuoteView(CreateView):
    form_class = QuoteForm
    template_name = "enquiries/quote.html"

    def get_initial(self):
        initial = super().get_initial()
        slug = self.request.GET.get("service")
        if slug:
            service = Service.objects.active().filter(slug=slug).first()
            if service:
                initial["service"] = service.pk
        return initial

    def form_valid(self, form):
        if form.is_spam():
            logger.info("Quote form honeypot filled; submission discarded.")
            return self.show_thanks(form.cleaned_data["name"])

        duplicate = Enquiry.objects.recent_duplicate_of(
            form.cleaned_data["email"], form.cleaned_data["project_description"]
        )
        if duplicate:
            logger.info("Duplicate quote submission ignored (matches enquiry %s).", duplicate.pk)
            return self.show_thanks(duplicate.name)

        enquiry = form.save()
        self.object = enquiry
        admin_url = self.request.build_absolute_uri(
            reverse("admin:enquiries_enquiry_change", args=[enquiry.pk])
        )
        # Only email once the enquiry is safely committed to the database.
        transaction.on_commit(lambda: send_enquiry_notification(enquiry, admin_url))
        return self.show_thanks(enquiry.name)

    def show_thanks(self, name):
        self.request.session[SUBMITTED_SESSION_KEY] = name
        return redirect("enquiries:quote_success")


class QuoteSuccessView(TemplateView):
    template_name = "enquiries/quote_success.html"

    def get(self, request, *args, **kwargs):
        name = request.session.pop(SUBMITTED_SESSION_KEY, None)
        if name is None:
            # Only reachable straight after a real submission.
            return redirect("enquiries:quote")
        return self.render_to_response(self.get_context_data(name=name))