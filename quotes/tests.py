import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from quotes.models import Author, Tag, Quote
from quotes.forms import AuthorForm, TagForm, QuoteForm
from quotes.templatetags.extract_tags import tagslist


@pytest.mark.django_db
class TestQuotesModels:
    def test_author_str(self):
        author = Author.objects.create(
            fullname="Albert Einstein",
            born_date="March 14, 1879",
            born_location="in Ulm, Germany",
            description="Theoretical physicist"
        )
        assert str(author) == "Albert Einstein"

    def test_tag_str(self):
        tag = Tag.objects.create(name="life")
        assert str(tag) == "life"

    def test_quote_str(self):
        author = Author.objects.create(fullname="Test Author")
        quote = Quote.objects.create(quote="Test quote content", author=author)
        # Considering real formatting __str__ of your model
        assert "Test quote content" in str(quote)
        assert "Test Author" in str(quote)


@pytest.mark.django_db
class TestQuotesForms:
    def test_author_form_valid(self):
        form = AuthorForm(data={
            'fullname': 'Isaac Newton',
            'born_date': 'January 4, 1643',
            'born_location': 'Woolsthorpe, UK',
            'description': 'Physicist and mathematician'
        })
        assert form.is_valid()

    def test_tag_form_valid(self):
        form = TagForm(data={'name': 'science'})
        assert form.is_valid()

    def test_quote_form_valid(self):
        author = Author.objects.create(fullname="Author For Form")
        tag = Tag.objects.create(name="physics")
        form = QuoteForm(data={
            'quote': 'Science is cool',
            'author': author.id,
            'tags': [tag.id]
        })
        assert form.is_valid()


@pytest.mark.django_db
class TestQuotesViews:
    @pytest.fixture
    def setup_data(self):
        user = User.objects.create_user(username='testuser', password='password123')
        author = Author.objects.create(fullname="Stephen Hawking")
        tag = Tag.objects.create(name="space")
        quote = Quote.objects.create(quote="Look up at the stars", author=author)
        quote.tags.add(tag)
        return user, author, tag, quote

    def test_index_view(self, client, setup_data):
        # If there is name of the main page 'main' in  urls.py , use 'quotes:main' or 'quotes:root'
        try:
            url = reverse('quotes:main')
        except Exception:
            url = reverse('quotes:root')
        response = client.get(url)
        assert response.status_code == 200

    def test_author_detail_view(self, client, setup_data):
        _, author, _, _ = setup_data
        
        # Send fullname of author instead of id/pk
        url = reverse('quotes:author', kwargs={'author_name': author.fullname})
        response = client.get(url)
        assert response.status_code == 200

    def test_quotes_by_tag_view(self, client, setup_data):
        try:
            url = reverse('quotes:quotes_by_tag', kwargs={'tag_name': 'space'})
        except Exception:
            url = reverse('quotes:tag', kwargs={'tag_name': 'space'})
        response = client.get(url)
        assert response.status_code == 200

    def test_add_author_view_unauthenticated(self, client):
        url = reverse('quotes:add_author')
        response = client.get(url)
        assert response.status_code == 302

    def test_add_author_view_authenticated(self, client, setup_data):
        user, _, _, _ = setup_data
        client.login(username='testuser', password='password123')
        
        response = client.get(reverse('quotes:add_author'))
        assert response.status_code == 200

        post_response = client.post(reverse('quotes:add_author'), {
            'fullname': 'Nikola Tesla',
            'born_date': 'July 10, 1856',
            'born_location': 'Smiljan, Austrian Empire',
            'description': 'Inventor'
        })
        assert post_response.status_code in (200, 302)

    def test_add_tag_view_authenticated(self, client, setup_data):
        user, _, _, _ = setup_data
        client.login(username='testuser', password='password123')
        
        response = client.post(reverse('quotes:add_tag'), {'name': 'energy'})
        assert response.status_code in (200, 302)

    def test_add_quote_view_authenticated(self, client, setup_data):
        user, author, tag, _ = setup_data
        client.login(username='testuser', password='password123')

        response = client.post(reverse('quotes:add_quote'), {
            'quote': 'Imagination is everything.',
            'author': author.id,
            'tags': [tag.id]
        })
        assert response.status_code in (200, 302)

    def test_add_author_invalid_post(self, client, setup_data):
        user, _, _, _ = setup_data
        client.force_login(user)  # Pass  user object
        response = client.post(reverse('quotes:add_author'), data={})
        assert response.status_code == 200
        assert response.context['form'].errors

    def test_add_quote_invalid_post(self, client, setup_data):
        user, _, _, _ = setup_data
        client.force_login(user)  
        response = client.post(reverse('quotes:add_quote'), data={})
        assert response.status_code == 200
        assert response.context['form'].errors

    def test_author_not_found(self, client, db):
        response = client.get(reverse('quotes:author', kwargs={'author_name': 'Non Existent Author'}))
        assert response.status_code in (404, 200)  # залежно від того, як реалізована 404 у views

    def test_pagination_out_of_bounds(self, client, db):
        url = reverse('quotes:main') + '?page=999'
        response = client.get(url)
        assert response.status_code == 200

    def test_extract_tags_filter_edge_cases(self, db):
        author = Author.objects.create(fullname="No Tag Author")
        quote = Quote.objects.create(quote="No tags here", author=author)

        # Передаємо quote.tags, а не сам quote
        result = tagslist(quote.tags)
        assert list(result) == []