import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from django.contrib.auth.models import User
from django.contrib.auth import login
from polls.models import Question, Choice

from datetime import datetime

from gradescope_utils.autograder_utils.decorators import weight

class AccountViewTests(TestCase):
    @weight(5)
    def test_login_logout_links(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "accounts/login")

    @weight(15)
    def test_login_page(self):
        get_response = self.client.get(reverse('login'))
        self.assertEqual(get_response.status_code, 200)
        self.assertContains(get_response, "Username")
        self.assertContains(get_response, "Password")
    
        User.objects.create_user(username='me', password='djangopony')
        post_response = self.client.post(reverse('login'), 
            {'username': 'me', 'password': 'djangopony'})
        self.assertEqual(post_response.status_code, 302)

    @weight(10)
    def test_logged_in_message(self):
        response = self.client.get(reverse('polls:index'))
        self.assertNotContains(response, 'Hello,')
        self.assertContains(response, 'accounts/login')
        self.assertNotContains(response, 'accounts/logout')

        user = User.objects.create_user(username='Ducky', password='djangopony')
        self.client.login(username='Ducky', password='djangopony')

        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, 'Hello, Ducky')
        self.assertNotContains(response, 'accounts/login')
        self.assertContains(response, 'accounts/logout')

    @weight(10)
    def test_signup_page(self):
        get_response = self.client.get(reverse('signup'))
        self.assertContains(get_response, 'Sign Up!')

        post_response = self.client.post(reverse('signup'), 
            {'username': 'Moxie', 'password1': 'djangopony', 'password2': 'djangopony'})
        self.assertEqual(post_response.status_code, 302)
        self.assertTrue(User.objects.filter(username='Moxie').exists())

class QuestionViewTests(TestCase):
    @weight(10)
    def test_question_creation_form(self):
        user = User.objects.create_user(username='Ducky', password='djangopony')
        self.client.login(username='Ducky', password='djangopony')

        get_response = self.client.get(reverse('polls:create'))
        self.assertEqual(get_response.status_code, 200)
        self.assertContains(get_response, 'New Poll')

        post_response = self.client.post(reverse('polls:create'), 
            {'question_text': 'Favorite dessert', 'pub_date': '1/1/2020'})
        self.assertEqual(post_response.status_code, 302)
        self.assertTrue(Question.objects.filter(question_text='Favorite dessert').exists())

    @weight(10)
    def test_save_question_author(self):
        get_response = self.client.get(reverse('polls:create'))
        self.assertEqual(get_response.status_code, 302)

        user = User.objects.create_user(username='Ducky', password='djangopony')
        self.client.login(username='Ducky', password='djangopony')

        post_response = self.client.post(reverse('polls:create'), 
            {'question_text': 'Favorite dessert', 'pub_date': '1/1/2020'})
        self.assertEqual(post_response.status_code, 302)
        self.assertTrue(Question.objects.filter(question_text='Favorite dessert').exists())
        
        question = Question.objects.get(question_text='Favorite dessert')
        self.assertEqual(question.author.username, 'Ducky')

    @weight(10)
    def test_choice_creation_form(self):
        user = User.objects.create_user(username='Ducky', password='djangopony')
        question = Question.objects.create(question_text='Favorite dessert', pub_date=datetime.now(), author=user)

        # form doesn't appear if user isn't the author
        get_response = self.client.get(reverse('polls:detail', args=[question.id]))
        self.assertEqual(get_response.status_code, 200)
        self.assertNotContains(get_response, 'Create a new Choice!')

        # form does appear if user is the author
        self.client.login(username='Ducky', password='djangopony')
        get_response = self.client.get(reverse('polls:detail', args=[question.id]))
        self.assertEqual(get_response.status_code, 200)
        self.assertContains(get_response, 'Create a new Choice!')

        # post is successful
        post_response = self.client.post(reverse('polls:detail', args=[question.id]),
            {'choice_text': 'Chocolate cake'})
        self.assertEqual(post_response.status_code, 302)
        self.assertTrue(question.choice_set.filter(choice_text='Chocolate cake').exists())

