import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Question, Choice

# Create your tests here.
class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date = time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        create_question(question_text="Past question.", days=-30)
        question = Question.objects.get(pk=1)
        question.choice_set.create(choice_text='Choice 1.', votes=0)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past question.>'])

    def test_future_question(self):
        create_question(question_text="Future question.", days=30)
        question = Question.objects.get(pk=1)
        question.choice_set.create(choice_text='Choice 1.', votes=0)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        create_question(question_text="Past question.", days=-30)
        question1 = Question.objects.get(pk=1)
        question1.choice_set.create(choice_text='Choice 1.', votes=0)
        create_question(question_text="Future question.", days=30)
        question2 = Question.objects.get(pk=2)
        question2.choice_set.create(choice_text='Choice 2.', votes=0)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past question.>'])

    def test_two_past_questions(self):
        create_question(question_text="Past question 1.", days=-30)
        question1 = Question.objects.get(pk=1)
        question1.choice_set.create(choice_text='Choice 1.', votes=0)
        create_question(question_text="Past question 2.", days=-5)
        question2 = Question.objects.get(pk=2)
        question2.choice_set.create(choice_text='Choice 2.', votes=0)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past question 2.>', '<Question: Past question 1.>'])

    def test_questions_with_choices(self):
        create_question(question_text="Question 1.", days=-5)
        question1 = Question.objects.get(pk=1)
        question1.choice_set.create(choice_text='Choice 1.', votes=0)
        create_question(question_text="Question 2.", days=-5)
        question2 = Question.objects.get(pk=2)
        question2.choice_set.create(choice_text='Choice 2.', votes=0)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],['<Question: Question 2.>', '<Question: Question 1.>']) 

    def test_questions_without_choices(self):
        create_question(question_text="Question 1.", days=-5)
        question1 = Question.objects.get(pk=1)
        question1.choice_set.create(choice_text='Choice 1.', votes=0)
        create_question(question_text="Question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],['<Question: Question 1.>'])   

class QuestionDetailView(TestCase):
    def test_future_question(self):
        future_question = create_question(question_text="Future question.", days=5)
        url = reverse('polls:detail', args=(future_question.id, ))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        past_question = create_question(question_text="Past question.", days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
