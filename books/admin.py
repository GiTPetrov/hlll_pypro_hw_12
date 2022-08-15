from books.models import Author, Book, Publisher, Store

from django.contrib import admin


class BookPathInline(admin.TabularInline):
    model = Book
    extra = 3


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'age')
    search_fields = ['name']
    list_filter = ['name', 'age']


class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'pages', 'price', 'rating', 'pubdate')
    fieldsets = [
        (None, {'fields': ['name']}),
        ('Book information', {'fields': ['authors', 'publisher', 'pages', 'rating', 'pubdate']}),
        ('Purchase', {'fields': ['price']}),
    ]
    list_filter = ['price', 'rating', 'pubdate']
    search_fields = ['name']


class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']
    list_filter = ['name']
    inlines = [BookPathInline]


class StoreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']
    list_filter = ['name']


admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Publisher, PublisherAdmin)
admin.site.register(Store, StoreAdmin)
