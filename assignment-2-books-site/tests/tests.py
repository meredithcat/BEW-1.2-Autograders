from django.test import TestCase

from gradescope_utils.autograder_utils.decorators import weight

from books.models import Book, Author, Tag

class ModelTests(TestCase):
    @weight(10)
    def test_book(self):
        b1 = Book.objects.create(title='Harry Potter', num_pages=300, date_published='1997-06-26')
        self.assertEqual(b1.title, 'Harry Potter')
    
    @weight(10)
    def test_author(self):
        a1 = Author.objects.create(name='J.K. Rowling', birth_date='1965-07-31')
        self.assertEqual(a1.name, 'J.K. Rowling')

    @weight(10)
    def test_book_author(self):
        a1 = Author.objects.create(name='J.K. Rowling', birth_date='1965-07-31')
        b1 = Book(title='Harry Potter', num_pages=300, date_published='1997-06-26')
        b1.author = a1
        b1.save()
        self.assertEqual(b1.author.name, 'J.K. Rowling')
    
    @weight(10)
    def test_tags(self):
        b1 = Book.objects.create(title='Harry Potter', num_pages=300, date_published='1997-06-26')
        t1 = Tag.objects.create(name='Fantasy')
        t2 = Tag.objects.create(name='Magic')
        b1.tags.add(t1)
        b1.tags.add(t2)
        b1.save()
        self.assertIn(t1, b1.tags.all())
        self.assertIn(t2, b1.tags.all())

class ViewTests(TestCase):
    @weight(10)
    def test_home(self):
        b1 = Book.objects.create(title='Little Women', num_pages=759, date_published='1868-09-30')
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Little Women')
        self.assertContains(response, 'book/1')
    
    @weight(4)
    def test_detail(self):
        a1 = Author.objects.create(name='Louisa May Alcott', birth_date='1832-11-29')
        b1 = Book.objects.create(title='Little Women', num_pages=759, date_published='1868-09-30', author=a1)
        response = self.client.get('/book/1/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '1868')
        self.assertContains(response, 'Little Women')
        self.assertContains(response, '759')
        self.assertContains(response, 'Louisa May Alcott')

    @weight(3)
    def test_detail_contains_authors_birth_date(self):
        a1 = Author.objects.create(name='Louisa May Alcott', birth_date='1832-11-29')
        b1 = Book.objects.create(title='Little Women', num_pages=759, date_published='1868-09-30', author=a1)
        response = self.client.get('/book/1/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '1832')

    @weight(3)
    def test_detail_contains_tags(self):
        a1 = Author.objects.create(name='Louisa May Alcott', birth_date='1832-11-29')
        b1 = Book.objects.create(title='Little Women', num_pages=759, date_published='1868-09-30', author=a1)
        b1.tags.add(Tag.objects.create(name='Fiction'))
        b1.tags.add(Tag.objects.create(name='Novel'))
        b1.save()
        response = self.client.get('/book/1/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Fiction')
        self.assertContains(response, 'Novel')


