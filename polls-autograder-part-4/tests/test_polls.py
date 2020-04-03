import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from polls.models import Question, Choice

from gradescope_utils.autograder_utils.decorators import weight

class QuestionModelTests(TestCase):    
    @weight(0)
    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    @weight(0)
    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

def create_choice(choice_text, question):
    return Choice.objects.create(choice_text=choice_text, question=question)


class QuestionIndexViewTests(TestCase):
    @weight(0)
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    @weight(0)
    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    @weight(0)
    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )

class QuestionDetailViewTests(TestCase):
    @weight(0)
    def test_no_questions(self):
        """
        The detail view of a question with id 10 returns a 404 not found.
        """
        url = reverse('polls:detail', args=[10])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    @weight(0)
    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

class VoteViewTests(TestCase):
    @weight(5)
    def test_vote_on_past_question(self):
        """
        Vote on past question, verify that vote count increases.
        """
        past_question = create_question(question_text='Past Question.', days=-5)
        choice1 = create_choice(choice_text='Banana.', question=past_question)
        choice2 = create_choice(choice_text='Strawberry.', question=past_question)
        choice3 = create_choice(choice_text='Orange.', question=past_question)

        url = reverse('polls:vote', args=[past_question.id])
        response = self.client.post(url, {'choice': '2'})

        # assert that we were redirected
        self.assertEqual(response.status_code, 302)

        selected_choice = Choice.objects.get(pk=choice2.id)
        self.assertEqual(selected_choice.votes, 1)

    @weight(5)
    def test_vote_no_choice(self):
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:vote', args=[past_question.id])
        response = self.client.post(url)

        self.assertContains(response, 'Past Question.')
        self.assertContains(response, 'select a choice.')