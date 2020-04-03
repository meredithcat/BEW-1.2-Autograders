import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from gradescope_utils.autograder_utils.decorators import weight


class QuestionIndexViewTests(TestCase):
    @weight(10)
    def test_index_view(self):
        """
        Check that the page renders with an appropriate message.
        """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Hello, world. You're at the polls index")

