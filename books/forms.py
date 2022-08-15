from books.models import Book

from django import forms


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'pages', 'price', 'rating', 'authors', 'publisher', 'pubdate']

    def send_email(self):
        # send email using the self.cleaned_data dictionary
        pass
