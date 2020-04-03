from django.test import TestCase

from gradescope_utils.autograder_utils.decorators import weight


class ViewTests(TestCase):
    @weight(15)
    def test_home(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Portfolio Home")

    @weight(10)
    def test_contact(self):
        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Contact Me")

    @weight(5)
    def test_greet_1(self):
        response = self.client.get('/greet/Meredith/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Meredith")

    @weight(5)
    def test_greet_2(self):
        response = self.client.get('/greet/Dani/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Dani")


    @weight(10)
    def test_message(self):
        response = self.client.get('/messages/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome to the message board")