from django import forms
from django.contrib.auth import get_user_model
from .models import Author, Quote, Tag


class QuoteFilterForm(forms.Form):
    filter_type = forms.ChoiceField(
        choices=[
            ("", "Filter quotes by..."),
            ("user", "User"),
            ("author", "Author"),
            ("tag", "Tag"),
        ],
        required=False,
        widget=forms.Select(attrs={"class": "form-select", "data-filter-type": ""}),
    )
    item = forms.ChoiceField(
        choices=[("", "Choose an item")],
        required=False,
        widget=forms.Select(attrs={"class": "form-select", "data-filter-item": "", "disabled": True}),
    )

    def __init__(self, *args, current_user=None, **kwargs):
        super().__init__(*args, **kwargs)
        selected_type = self.data.get("filter_type") or self.initial.get("filter_type", "")
        user_model = get_user_model()
        self.filter_options = {
            "user": [
                [
                    str(user.pk),
                    "me" if current_user and user.pk == current_user.pk else user.get_username(),
                ]
                for user in user_model.objects.order_by("username")
            ],
            "author": [
                [str(author.pk), author.fullname]
                for author in Author.objects.order_by("fullname")
            ],
            "tag": [
                [str(tag.pk), tag.name]
                for tag in Tag.objects.order_by("name")
            ],
        }
        if selected_type in self.filter_options:
            self.fields["item"].choices = [
                ("", "Choose an item"),
                *self.filter_options[selected_type],
            ]


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
        widget=forms.CheckboxSelectMultiple(attrs={"class": "tags-checkboxes"}),
        required=False
    )

    class Meta:
        model = Quote
        fields = ["quote", "author", "tags"]
        widgets = {
            "quote": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Enter quote text"}),
        }