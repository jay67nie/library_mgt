from django.http import HttpResponse
from django.test import TestCase, Client
from django.urls import reverse
from django.test import RequestFactory

from .forms import Login_form
from .models import book
from datetime import date
from django.contrib.auth.models import User


class BookModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        book.objects.create(publication_date=date.today(), author='John Doe',
                            subject_area='Science', title='Introduction to Science',
                            shelf_number='A1', borrowed=False)

    def test_title_label(self):
        book_obj = book.objects.get(id=1)
        field_label = book_obj._meta.get_field('title').verbose_name
        self.assertEquals(field_label, 'title')

    def test_author_label(self):
        book_obj = book.objects.get(id=1)
        field_label = book_obj._meta.get_field('author').verbose_name
        self.assertEquals(field_label, 'author')

    def test_subject_area_label(self):
        book_obj = book.objects.get(id=1)
        field_label = book_obj._meta.get_field('subject_area').verbose_name
        self.assertEquals(field_label, 'subject area')

    def test_shelf_number_label(self):
        book_obj = book.objects.get(id=1)
        field_label = book_obj._meta.get_field('shelf_number').verbose_name
        self.assertEquals(field_label, 'shelf number')

    def test_book_borrowed_default_value(self):
        book_obj = book.objects.get(id=1)
        borrowed = book_obj.borrowed
        self.assertFalse(borrowed)


class BorrowViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.book = book.objects.create(
            publication_date=date.today(),
            author='John Doe',
            subject_area='Science',
            title='Test Book',
            shelf_number='A1',
            borrowed=False
        )

    def test_borrow_view_with_unauthenticated_user(self):
        url = reverse('borrow', args=[self.book.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/')

    def test_borrow_view_with_authenticated_user(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('borrow', args=[self.book.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'borrow.html')
        self.assertContains(response, self.book.title)

    def test_borrow_view_with_borrowed_book(self):
        self.book.borrowed = True
        self.book.save()
        self.client.login(username='testuser', password='testpass')
        url = reverse('borrow', args=[self.book.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/index/')


class LogInViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_log_in_get_request(self):
        response = self.client.get('/login', follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, HttpResponse)
        self.assertIsInstance(response.context['form'], Login_form)
        self.assertNotIn('obj', response.context)
        # Add more assertions as needed

    def test_log_in_post_request(self):
        response = self.client.post('/login', {'user_name': 'myuser', 'password': 'mypassword'}, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, HttpResponse)
        self.assertIsInstance(response.context['form'], Login_form)
        self.assertNotIn('obj', response.context)
        # Add more assertions as needed


