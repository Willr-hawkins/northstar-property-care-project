import re
from django import forms

from services.models import Service
from .models import Enquiry

UK_POSTCODE = re.compile(r"^[A-Z]{1,2}\d[A-Z\d]?\d[A-Z]{2}$")
UK_PHONE = re.compile(r"^(?:\+44|0)\d{9,10}$")

INPUT_CLASSES = (
    "form-input min-h-12 w-full rounded-xs border border-charcoal/35 bg-offwhite px-3.5 "
    "text-base text-charcoal aria-invalid:border-2 aria-invalid:border-terracotta-deep"
)


class QuoteForm(forms.ModelForm):
    service = forms.ModelChoiceField(
        queryset=Service.objects.active(),
        required=False,
        empty_label="Not sure yet",
    )
    preferred_contact_method = forms.ChoiceField(
        label="How should we contact you?",
        choices=Enquiry.ContactMethod.choices,
        widget=forms.RadioSelect,
        required=False,
        initial=Enquiry.ContactMethod.EMAIL,
    )

    class Meta:
        model = Enquiry
        fields = [
            "name", "email", "phone", "service",
            "postcode", "project_description", "preferred_contact_method",
        ]
        labels = {
            "name": "Your name",
            "email": "Email",
            "phone": "Phone",
            "postcode": "Postcode",
            "project_description": "About your project",
        }
        help_texts = {
            "project_description": "What would you like done, and roughly when? Room sizes help if you know them.",
        }
        widgets = {
            "project_description": forms.Textarea(attrs={"rows": 6}),
        }
        error_messages = {
            "name": {"required": "Enter your name"},
            "email": {
                "required": "Enter your email address",
                "invalid": "Enter an email address in the format name@example.com",
            },
            "postcode": {"required": "Enter your postcode"},
            "project_description": {"required": "Tell us a little about your project"},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        autocomplete = {"name": "name", "email": "email", "phone": "tel", "postcode": "postal-code"}

        for name, field in self.fields.items():
            if name == "preffered_contact_method":
                continue
            field.widget.attrs["class"] = INPUT_CLASSES
            if name in autocomplete:
                field.widget.attrs["autocomplete"] = autocomplete[name]
            if field.help_text:
                field.widget.attrs["aria-describedby"] = f"id_{name}_helptext"
            
        self.fields["postcode"].widget.attrs["class"] += " uppercase"
        self.fields["project_description"].widget.attrs["class"] += " py-3 leading-relaxed"

    def full_clean(self):
        """After validating, link each invalid field to its error message for screen readers."""
        super().full_clean()
        for name in self.errors:
            if name not in self.fields:
                continue
            attrs = self.fields[name].widget.attrs
            attrs["aria-invalid"] = "true"
            described_by = [f"id_{name}_error"]
            if self.fields[name].help_text:
                described_by.append(f"id_{name}_helptext")
            attrs["aria-describedby"] = " ".join(described_by)


    # --- Field validation -------------------------------------------------

    def clean_name(self):
        name = " ".join(self.cleaned_data["name"].split())
        if len(name) < 2:
            raise forms.ValidationError("Enter your full name")
        return name

    def clean_email(self):
        return self.cleaned_data["email"].strip().lower()

    def clean_phone(self):
        phone = self.cleaned_data.get("phone", "").strip()
        if not phone:
            return ""
        digits = re.sub(r"[\s\-()]", "", phone)
        if not UK_PHONE.match(digits):
            raise forms.ValidationError("Enter a UK phone number, like 07700 900123")
        return phone

    def clean_postcode(self):
        compact = re.sub(r"\s", "", self.cleaned_data["postcode"]).upper()
        if not UK_POSTCODE.match(compact):
            raise forms.ValidationError("Enter a valid UK postcode, like BS8 1AA")
        return f"{compact[:-3]} {compact[-3:]}"

    def clean_project_description(self):
        description = self.cleaned_data["project_description"].strip()
        if len(description) < 20:
            raise forms.ValidationError("Tell us a little more about your project, at least a sentence or two")
        return description

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("preferred_contact_method") == Enquiry.ContactMethod.PHONE and not cleaned.get("phone"):
            self.add_error("phone", "Enter a phone number, or choose email as your contact method")
        return cleaned