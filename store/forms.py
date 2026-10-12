from django import forms
from .models import Review, Order, ContactMessage, NewsletterSubscriber


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["author_name", "rating", "title", "comment"]
        widgets = {
            "author_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Your Name"}),
            "rating": forms.Select(attrs={"class": "form-control"}),
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Headline of your review"}),
            "comment": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Share your tasting experience..."}),
        }


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            "full_name",
            "email",
            "phone",
            "address",
            "city",
            "state",
            "postal_code",
            "payment_method",
            "notes",
        ]
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Full Name", "required": True}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email Address", "required": True}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "Phone Number", "required": True}),
            "address": forms.TextInput(attrs={"class": "form-control", "placeholder": "Street Address & House / Apt #", "required": True}),
            "city": forms.TextInput(attrs={"class": "form-control", "placeholder": "City", "required": True}),
            "state": forms.TextInput(attrs={"class": "form-control", "placeholder": "State / Province", "required": True}),
            "postal_code": forms.TextInput(attrs={"class": "form-control", "placeholder": "Postal Code", "required": True}),
            "payment_method": forms.Select(attrs={"class": "form-control"}),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 2, "placeholder": "Special delivery instructions (optional)"}),
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "subject", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Your Name", "required": True}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Your Email", "required": True}),
            "subject": forms.TextInput(attrs={"class": "form-control", "placeholder": "Subject", "required": True}),
            "message": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "How can we assist you?", "required": True}),
        }


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscriber
        fields = ["email"]
        widgets = {
            "email": forms.EmailInput(attrs={"class": "newsletter-input", "placeholder": "Enter your email address...", "required": True}),
        }
