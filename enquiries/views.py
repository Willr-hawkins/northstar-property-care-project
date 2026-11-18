from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from services.models import Service

from .forms import QuoteForm

SUBMITTED_SESSION_KEY = "quote_submitted_name"


class QuoteView(CreateView):
    form_class = QuoteForm
    template_name = "enquiries/quote.html"
    success_url = reverse_lazy("enquiries:quote_success")

    def get_initial(self):
        initial = super().get_initial()
        slug = self.request.GET.get("service")
        if slug:
            service = Service.objects.active().filter(slug=slug).first()
            if service:
                initial["service"] = service.pk
        return initial

    def form_valid(self, form):
        response = super().form_valid(form)  # saves the enquiry
        self.request.session[SUBMITTED_SESSION_KEY] = self.object.name
        return response


class QuoteSuccessView(TemplateView):
    template_name = "enquiries/quote_success.html"

    def get(self, request, *args, **kwargs):
        name = request.session.pop(SUBMITTED_SESSION_KEY, None)
        if name is None:
            # Only reachable straight after a real submission.
            return redirect("enquiries:quote")
        return self.render_to_response(self.get_context_data(name=name))