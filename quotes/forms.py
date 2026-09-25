from django import forms
from .models import Author, Quote, Tag


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ["fullname", "born_date", "born_location", "description"]
        widgets = {
            "fullname": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter fullname"}),
            "born_date": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. January 15, 1929"}),
            "born_location": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. in Atlanta, Georgia"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 5, "placeholder": "Enter author description"}),
        }


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter tag name"}),
        }

    def clean_name(self):
        name = self.cleaned_data.get("name", "").strip().lower()
        if Tag.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError("Tag with this name already exists.")
        return name


class QuoteForm(forms.ModelForm):
    author = forms.ModelChoiceField(
        queryset=Author.objects.all(),
        widget=forms.Select(attrs={"class": "form-select"}),
        empty_label="Select an author",
        required=True
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.SelectMultiple(attrs={"class": "form-select", "size": "6"}),
        required=False
    )

    class Meta:
        model = Quote
        fields = ["quote", "author", "tags"]
        widgets = {
            "quote": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Enter quote text"}),
        }