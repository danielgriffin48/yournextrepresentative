from django import forms
from django.core.exceptions import ValidationError

from duplicates.models import DuplicateSuggestion


class DuplicateSuggestionForm(forms.ModelForm):
    class Meta:
        model = DuplicateSuggestion
        fields = ["other_person"]
        widgets = {"other_person": forms.HiddenInput()}
        error_messages = {
            "other_person": {
                "invalid_choice": "The other person ID provided was invalid",
                "required": "Other person ID was not provided",
            }
        }

    def __init__(self, *args, **kwargs):
        person = kwargs.pop("person")
        user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        self.instance.person = person
        self.instance.user = user

    def clean(self):
        cleaned_data = super().clean()
        other_person = cleaned_data.get("other_person")

        if not other_person:
            return cleaned_data

        if self.instance.person.pk == other_person.pk:
            msg = f"You can't suggest a duplicate person ({self.instance.person.pk}) with themself ({other_person.pk})"
            self.add_error(field="other_person", error=msg)

        existing_suggestion = DuplicateSuggestion.objects.for_both_people(
            person=self.instance.person, other_person=other_person
        ).first()
        if not existing_suggestion:
            return cleaned_data

        if existing_suggestion.open:
            raise ValidationError(
                "A suggestion between these people is already open"
            )

        if existing_suggestion.rejected:
            msg = (
                "A suggestion between these two people has already been "
                "checked and rejected as not duplicate because: "
                f"{existing_suggestion.rejection_reasoning}"
            )
            raise ValidationError(msg)


class RejectionForm(forms.ModelForm):
    class Meta:
        model = DuplicateSuggestion
        fields = ["rejection_reasoning"]
        labels = {"rejection_reasoning": "Reason"}
        widgets = {
            "rejection_reasoning": forms.Textarea(
                attrs={
                    "placeholder": "Please explain your reasons for rejecting this suggestion"
                }
            )
        }

    def save(self, commit=True):
        """
        This is a rejection form so alwasy set status to NOT_DUPLICATE before
        saving
        """
        self.instance.status = DuplicateSuggestion.NOT_DUPLICATE
        return super().save(commit=commit)
