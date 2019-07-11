from django.test import Client, TestCase

from .models import Post


class PostModelTests(TestCase):

    def test_slug(self):
        p = Post(title='How to run tests in Django', content='Just import TestCase')
        p.save()
        self.assertEqual(p.slug, 'how-to-run-tests-in-django')

    def test_memoize_slug(self):
        p = Post(title='How to run tests in Django', content='Just import TestCase')
        p.save()

        p.title = 'How NOT to run a single test in Django and wing it instead'
        p.make_published()
        p.save()
        self.assertEqual(p.slug, 'how-to-run-tests-in-django')

    def test_private(self):
        p = Post(title='How to run tests in Django', content='Just import TestCase')
        p.make_published() # also save()s

        c = Client()
        html = c.get('/how-to-run-tests-in-django/').content.decode("utf-8")
        self.assertInHTML('<h1>How to run tests in Django </h1>', html)