from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import DeleteView, UpdateView
from django.contrib import messages
from django.db.models import Count
from django.urls import reverse_lazy

from .models import Quote, Author, Tag
from .forms import AuthorForm, QuoteForm, TagForm

PER_PAGE = 10


def main(request, page=1):
    quotes_list = Quote.objects.select_related(
        'author', 'created_by'
    ).prefetch_related('tags')
    paginator = Paginator(quotes_list, per_page=PER_PAGE)
    quotes_page = paginator.get_page(page)

    top_tags = Tag.objects.annotate(num_quotes=Count('quotes')).order_by('-num_quotes')[:10]

    context = {
        "quotes": quotes_page,
        "top_tags": top_tags,
    }
    return render(request, "quotes/index.html", context)


def author(request, author_name: str):
    author_obj = get_object_or_404(Author, fullname=author_name)
    return render(request, "quotes/author.html", {"author": author_obj})


def tag(request, tag_name: str, page: int = 1):
    tag_obj = get_object_or_404(Tag, name=tag_name)
    quotes_list = Quote.objects.filter(tags=tag_obj).select_related(
        'author', 'created_by'
    ).prefetch_related('tags')
    
    paginator = Paginator(quotes_list, per_page=PER_PAGE)
    quotes_page = paginator.get_page(page)

    top_tags = Tag.objects.annotate(num_quotes=Count('quotes')).order_by('-num_quotes')[:10]

    context = {
        "quotes": quotes_page,
        "tag_query": tag_name,
        "top_tags": top_tags,
    }
    return render(request, "quotes/tag.html", context)


class AddAuthorView(LoginRequiredMixin, View):
    form_class = AuthorForm
    template_name = "quotes/add_author.html"

    def get(self, request):
        return render(request, self.template_name, {"form": self.form_class()})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            author_obj = form.save()
            messages.success(request, f"Author '{author_obj.fullname}' was successfully created!")
            return redirect("quotes:main")
        
        messages.error(request, "Please correct the errors below.")
        return render(request, self.template_name, {"form": form})


class AddTagView(LoginRequiredMixin, View):
    form_class = TagForm
    template_name = "quotes/add_tag.html"

    def get(self, request):
        return render(request, self.template_name, {"form": self.form_class()})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            tag_obj = form.save()
            messages.success(request, f"Tag '{tag_obj.name}' was successfully created!")
            return redirect("quotes:main")
        
        messages.error(request, "Please correct the errors below.")
        return render(request, self.template_name, {"form": form})


class AddQuoteView(LoginRequiredMixin, View):
    form_class = QuoteForm
    template_name = "quotes/add_quote.html"

    def get(self, request):
        return render(request, self.template_name, {"form": self.form_class()})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            quote_obj = form.save(commit=False)
            quote_obj.created_by = request.user
            quote_obj.save()
            form.save_m2m()
            messages.success(request, "Quote was successfully added!")
            return redirect("quotes:main")
        
        messages.error(request, "Failed to add quote. Please check the form.")
        return render(request, self.template_name, {"form": form})


class QuoteOwnerMixin(LoginRequiredMixin):
    def get_queryset(self):
        queryset = Quote.objects.all()
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(created_by=self.request.user)


class EditQuoteView(QuoteOwnerMixin, UpdateView):
    model = Quote
    form_class = QuoteForm
    template_name = "quotes/add_quote.html"
    pk_url_kwarg = "quote_id"

    def form_valid(self, form):
        messages.success(self.request, "Quote was successfully updated.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("quotes:main")


class DeleteQuoteView(QuoteOwnerMixin, DeleteView):
    model = Quote
    template_name = "quotes/delete_quote.html"
    pk_url_kwarg = "quote_id"
    success_url = reverse_lazy("quotes:main")

    def form_valid(self, form):
        messages.success(self.request, "Quote was successfully deleted.")
        return super().form_valid(form)