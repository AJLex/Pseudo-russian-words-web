import random

from django.utils import timezone
from django.template import loader
from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.models import User
from .models import IndexTable, PseudoWord


def get_words(limit, number_of_syllables):
    word=''
    status = True
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
    return word, status


def index(request):
    word = ''
    form = request.POST
    context = {'word': '', 'username': auth.get_user(request).username}
    print(auth.get_user(request).username)
    show_words = PseudoWord.objects.filter(user__username=auth.get_user(request).username)
    context['show_words'] = show_words
    if form.get('limit') and form.get('number_of_syllables'):
            word, status = get_words(form.get('limit'), form.get('number_of_syllables'))
            if status:
                context['word'] = word
                if not PseudoWord.objects.filter(word=word) and word != '':
                    w = PseudoWord(word=word, add_date=timezone.now())
                    w.save()
            else:
                context['word'] = 'Измените параметры'
    last_words = PseudoWord.objects.order_by('-add_date')[:5]
    context['last_words'] = last_words
    if request.user.is_authenticated():
        u = User.objects.get(username=auth.get_user(request).username)
        if form.get('word_to_add'):
            word_to_add = form.get('word_to_add')
            w = PseudoWord.objects.get(word=word_to_add)
            w.user.add(u)
        #     show_words = PseudoWord.objects.filter(user__username=auth.get_user(request).username)
        #     context['show_words'] = show_words
    return render(request,'words/index.html', context)
    # else:
    #     return render(request,'words/index.html', context)
