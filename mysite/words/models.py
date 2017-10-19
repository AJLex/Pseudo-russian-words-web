from django.db import models
from django.contrib.auth.models import User


class WordsDictionary(models.Model):
    word = models.CharField(max_length=30)

    def __str__(self):
        return self.syllable


class IndexTable(models.Model):
    syllable = models.CharField(max_length=20)
    previous_syllable = models.CharField(max_length=20)
    syllable_index = models.IntegerField(default=0)
    number_of_syllables = models.IntegerField(default=0)
    count_syllable = models.IntegerField(default=0)

    def __str__(self):
        return self.syllable


class PseudoWord(models.Model):
    word = models.CharField(max_length=20)
    add_date = models.DateTimeField('add date')
    user = models.ManyToManyField(User)

    def __str__(self):
        return self.word
