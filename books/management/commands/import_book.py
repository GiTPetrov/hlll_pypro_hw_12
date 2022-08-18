import datetime
import random

from books.models import Author, Book, Publisher, Store

from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string


def parcelling(times, parcel_objects_sum):
    parc_object_list = list()
    for num, item in enumerate(range(times)):
        if item != times - 1:
            a = times - num
            b = parcel_objects_sum * random.randrange(1, 100) // 100 // a * a
            parc_object_list.append(b)
            parcel_objects_sum -= b
        else:
            parc_object_list.append(parcel_objects_sum)
    len_parcel_books = len(parc_object_list)
    one_objects_sum = 0
    parc_one_object_list = list()
    for num, item in enumerate(parc_object_list):
        parc_one_object_list.append(item // (len_parcel_books - num))
        one_objects_sum += item // (len_parcel_books - num)
    return one_objects_sum, parc_one_object_list, parc_object_list


def many_to_many_create(times, parceling_list, one_objects_list, many_objects_list):
    another_one_objects_list = list()
    another_many_objects_list = list()
    for item in range(times):
        for unit in range(parceling_list[item]):
            auth = one_objects_list.pop(random.randrange(0, len(one_objects_list)))
            i = 0
            while i < times - item:
                b = many_objects_list.pop(random.randrange(0, len(many_objects_list)))
                auth.book_set.add(b)
                i += 1
                another_many_objects_list.append(b)
            another_one_objects_list.append(auth)
    return another_one_objects_list, set(another_many_objects_list)


def m_to_m_cobooks_coauthors(times, cobooks_set, co_authors_set):
    another_co_books_set = set()
    another_co_authors_set = set()
    for item in range(2, times):
        if item != times - 1:
            i = 0
            while i < len(cobooks_set) * random.randrange(1, 40) // 100:
                cobook = cobooks_set.pop()
                coaut_set = random.sample(co_authors_set, item)
                for unt in coaut_set:
                    cobook.authors.add(unt)
                    another_co_authors_set.add(unt)
                another_co_books_set.add(cobook)
        else:
            i = 0
            coaut_diff = set()
            while i < len(cobooks_set) - 1:
                cobook = cobooks_set.pop()
                coaut_diff = co_authors_set.difference(another_co_authors_set)
                if len(coaut_diff) // 2 > 1:
                    coaut_set = random.sample(coaut_diff, len(coaut_diff) // 2)
                else:
                    coaut_set = random.sample(co_authors_set, item)
                for unt in coaut_set:
                    cobook.authors.add(unt)
                    another_co_authors_set.add(unt)
                another_co_books_set.add(cobook)
            cobook = cobooks_set.pop()
            for unt in coaut_diff:
                cobook.authors.add(unt)
                another_co_authors_set.add(unt)
            another_co_books_set.add(cobook)
    diff_set = co_authors_set.difference(another_co_authors_set)
    return diff_set, another_co_books_set, another_co_authors_set


def m_to_m_store_books(stores_set, books_set):
    times = len(books_set)
    for unit in stores_set:
        bk_set = random.sample(books_set, random.randrange(0, times))
        for item in bk_set:
            unit.books.add(item)


def foreignkey_publisher_book(publisher_set, books_set):
    times = len(books_set) // len(publisher_set) * 2
    another_books_set = set()
    for num, item in enumerate(publisher_set, start=1):
        if num != len(publisher_set):
            while True:
                j = random.randrange(1, times)
                if j < len(books_set) + 1:
                    break
            i = 0
            while i < j:
                bk = books_set.pop()
                item.book_set.add(bk)
                another_books_set.add(bk)
                i += 1
        else:
            i = 0
            while i < len(books_set):
                bk = books_set.pop()
                item.book_set.add(bk)
                another_books_set.add(bk)
    return another_books_set


def rand_date():
    start_date = datetime.date(1980, 1, 1)
    end_date = datetime.date(2021, 12, 31)

    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + datetime.timedelta(days=random_number_of_days)
    return random_date


percent_co_books = 20
percent_authors = 50
percent_coauthors = 60
percent_null_coauthors = 40
min_stores = 5
max_stores = 10
percent_publishers = 30
negative_deviation = 10

one_book_num_coauthors = 4
one_author_books_max = 3


class Command(BaseCommand):
    help = 'Create some random books'  # noqa: A003

    def add_arguments(self, parser):
        parser.add_argument(
            'num_books',
            type=int,
            choices=range(30, 5000),
            help='Sets the number of users to create')

    def handle(self, *args, **options):
        import_id = get_random_string(length=4)
        books = options['num_books']
        co_books = books * random.randrange(percent_co_books - negative_deviation, percent_co_books) // 100
        books_one_author = books - co_books
        stores = random.randrange(min_stores, max_stores)
        publishers = books * random.randrange(percent_publishers - negative_deviation, percent_publishers) // 100
        authors, auth_parc, _ = parcelling(one_author_books_max, books_one_author)
        coauthors = authors * random.randrange(percent_coauthors - negative_deviation, percent_coauthors) // 100
        null_coauthors = coauthors * random.randrange(
            percent_null_coauthors - negative_deviation, percent_null_coauthors
        ) // 100

        authors_list = [
            Author(name=f'Author-{import_id}-{item}', age=random.randrange(20, 70)) for item in range(authors)
        ]
        Author.objects.bulk_create(authors_list)
        publishers_list = [Publisher(name=f'Publisher-{import_id}-{item}') for item in range(publishers)]
        Publisher.objects.bulk_create(publishers_list)
        publishers_set = set(publishers_list)
        stores_list = [Store(name=f'Store-{import_id}-{item}') for item in range(stores)]
        Store.objects.bulk_create(stores_list)
        stores_set = set(stores_list)
        coauthors_lst = [Author(
            name=f'Сo-author-ONLY-{import_id}-{item}',
            age=random.randrange(20, 70)) for item in range(null_coauthors)]
        Author.objects.bulk_create(coauthors_lst)
        coauthors_set = set(coauthors_lst)
        co_set = set(random.sample(authors_list, k=coauthors - null_coauthors))
        coauthors_set.update(co_set)

        books_one_author_list = [
            Book(
                name=f'Book-{import_id}-{item}',
                pages=random.randrange(50, 600),
                price=random.randrange(10, 200, 15),
                rating=0,
                pubdate=rand_date(),
                publisher_id=1
            ) for item in range(books_one_author)
        ]
        Book.objects.bulk_create(books_one_author_list)
        co_books_lst = [
            Book(
                name=f'Co-book-{import_id}-{item}',
                pages=random.randrange(50, 600),
                price=random.randrange(10, 200),
                rating=0,
                pubdate=rand_date(),
                publisher_id=1
            ) for item in range(co_books)
        ]
        Book.objects.bulk_create(co_books_lst)
        co_books_set = set(co_books_lst)
        another_authors_list, another_books_one_author_list = many_to_many_create(
            one_author_books_max,
            auth_parc,
            authors_list,
            books_one_author_list
        )
        dif_set, ano_cobook_set, ano_coaut_set = m_to_m_cobooks_coauthors(
            one_book_num_coauthors,
            co_books_set,
            coauthors_set
        )
        book_set = set(another_books_one_author_list)

        ano_cobook_set.update(book_set)
        ano_cobook_set = foreignkey_publisher_book(publishers_set, ano_cobook_set)
        m_to_m_store_books(stores_set, ano_cobook_set)
