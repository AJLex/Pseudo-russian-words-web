# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-18 16:25
from __future__ import unicode_literals

import csv

from django.db import migrations


def filling_WordsDictionary(apps, schema_editor):
    file_read = "words/freqrnc2011.csv"
    WordsDictionary = apps.get_model('words', 'WordsDictionary')
    with open(file_read, 'r', encoding='utf-8') as f:
        syllable_list = []
        fields = ['word', 'PoS', 'Freq', 'R', 'D', 'Doc']
        reader = csv.DictReader(f, fields, delimiter='	')
        for row in reader:
            w = WordsDictionary(
            word = row.get('word')
            )
            w.save()


class Migration(migrations.Migration):

    dependencies = [
        ('words', '0004_wordsdictionary'),
    ]

    operations = [
        migrations.RunPython(filling_WordsDictionary),
    ]
