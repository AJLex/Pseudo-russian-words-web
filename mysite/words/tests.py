from django.test import TestCase
from .models import IndexTable, PseudoWord, WordsDictionary
from views import get_words


class QuestionMethodTests(TestCase):

    def test_get_words(self):
