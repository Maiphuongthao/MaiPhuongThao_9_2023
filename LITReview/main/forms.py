from django import forms
from .models import Ticket, Review


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["headline", "rating", "body"]
        labels = {"headline": "Titre", "rating": "Note", "body": "Commentaire"}
        choices = [
            (0, "0"),
            (1, "1"),
            (2, "2"),
            (3, "3"),
            (4, "4"),
            (5, "5"),
        ]
        widgets = {
            "rating": forms.RadioSelect(choices=choices, attrs={"class": ""}),
            "body": forms.Textarea(),
        }
