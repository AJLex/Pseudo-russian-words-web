import random

from django.utils import timezone
from django.template import loader
from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.models import User
from .models import IndexTable, PseudoWord, WordsDictionary


"""
Function gets pseudo words from set of syllables.
"""
def get_words(limit, number_of_syllables, status):
    while True:
        word=''
        previous_syllable = 'BEG'
        for index in range(int(number_of_syllables)):
            syllables = IndexTable.objects.filter(
                previous_syllable=previous_syllable,
                syllable_index=index,
                number_of_syllables=number_of_syllables
            ).order_by('count_syllable').reverse()
            try:
                syllable_selected = syllables[
                    random.randint(0, int(len(syllables)*int(limit)*0.01))
                ].syllable
                word += syllable_selected
                previous_syllable = syllable_selected
            except:
                status = False
                break        
        if not WordsDictionary.objects.filter(word=word):
            break
    return word, status


"""
Function gets pseudo word after pushing button "Вперёд"
"""
def start_button_handler(form, context):
    status = True
    if form.get('limit') and form.get('number_of_syllables'):
        word, status = get_words(
            form.get('limit'),
            form.get('number_of_syllables'),
            status
        )
        if status:
            context['word'] = word
            if not PseudoWord.objects.filter(word=word) and word != '':
                w = PseudoWord(word=word, add_date=timezone.now())
                w.save()
        else:
            context['word'] = 'Измените параметры'
    return context, status


"""
Function gets last 5 pseudo words from data base
"""
def get_last_words(context):
    last_words = PseudoWord.objects.order_by('-add_date')[:5]
    context['last_words'] = last_words
    return context


"""
Function saves words into database when user push button "Сохранить слово"
"""
def save_word(request, form, status):
    u = User.objects.get(username=auth.get_user(request).username)
    if form.get('word_to_add') and status:
        word_to_add = form.get('word_to_add')
        w = PseudoWord.objects.get(word=word_to_add)
        w.user.add(u)


def index(request):
    status = False
    form = request.POST
    context = {'word': '', 'username': auth.get_user(request).username}
    context['show_words'] = PseudoWord.objects.filter(
        user__username=auth.get_user(request).username
    )
    if form.get('get_word'):
        context, status = start_button_handler(form, context)
    context = get_last_words(context)
    if request.user.is_authenticated():
        save_word(request, form, status)
    return render(request,'words/index.html', context)
