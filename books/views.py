from books.forms import BookForm
from books.models import Author, Book, Publisher, Store

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg, Count, Max
from django.shortcuts import render
from django.views import generic


def index(request):
    return render(request, 'books/index.html', {})


class AuthorInfo(generic.DetailView):
    model = Author
    slug_field = "name"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author_book'] = Book.objects.filter(authors=self.object)
        return context


class AuthorsList(generic.ListView):
    queryset = Author.objects.annotate(
        num_books=Count('book', distinct=True),
        max_price=Max('book__price'),
        avg_pages=Avg('book__pages'),
    )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['num_authors'] = Author.objects.count()
        context['agr'] = Author.objects.aggregate(avg_age=Avg('age'))
        return context


class BookInfo(generic.DetailView):
    model = Book
    slug_field = "name"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stores_without_book'] = Store.objects.exclude(books=self.object)
        return context


class BookFormCreateView(LoginRequiredMixin, generic.CreateView):
    model = Book
    slug_field = "name"
    login_url = '/accounts/login'
    template_name = 'books/book_form.html'
    form_class = BookForm
    success_url = '/book-list/'


class BookFormView(generic.edit.ModelFormMixin, generic.detail.BaseDetailView, generic.base.TemplateView):
    model = Book
    slug_field = "name"
    template_name = 'books/book_form_view.html'
    form_class = BookForm


class BookFormUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Book
    slug_field = "name"
    login_url = '/accounts/login'
    template_name = 'books/book_form.html'
    form_class = BookForm
    success_url = '/book-list/'


class BookFormDeleteView(LoginRequiredMixin, generic.edit.ModelFormMixin, generic.DeleteView):
    model = Book
    slug_field = "name"
    login_url = '/accounts/login'
    template_name = 'books/book_form_del.html'
    form_class = BookForm
    success_url = '/book-list/'


class BooksList(generic.ListView):
    queryset = Book.objects.annotate(
            num_authors=Count('authors', distinct=True),
            num_publishers=Count('publisher', distinct=True),
            num_stores=Count('store', distinct=True),
        )
    context_object_name = 'object_list'
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        strs = Store.objects.prefetch_related('books')
        s = len(strs)
        i = 0
        for b in self.object_list:
            a = strs.exclude(books=b.id).count()
            if a == s:
                i += 1
        context['books_without_stores'] = i
        context['num_books'] = Book.objects.count()
        return context


class PublisherInfo(generic.DetailView):
    model = Publisher
    slug_field = "name"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['publ_book'] = Book.objects.filter(publisher=self.object)
        return context


class PublishersList(generic.ListView):
    queryset = Publisher.objects.annotate(
        num_books=Count('book', distinct=True),
        num_authors=Count('book__authors'),
        avg_rating=Avg('book__rating'),
    )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['num_publisher'] = Publisher.objects.count()
        return context


class StoreInfo(generic.DetailView):
    model = Store
    slug_field = "name"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books_notin_store'] = Book.objects.exclude(store=self.object)
        return context


class StoresList(generic.ListView):
    queryset = Store.objects.annotate(
        num_books=Count('books', distinct=True),
        avg_price=Avg('books__price'),
    )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['num_stores'] = Store.objects.count()
        return context
