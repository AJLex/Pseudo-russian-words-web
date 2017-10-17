import random
import csv
from collections import Counter


'''
basic variables:
    current_letter_number - current letter in cicle "for"
                            inside function get_word_by_syllable
    letter_number - len of variable "word"
    word - sum of syllables
    word_by_syllables - list of syllables
    word_by_letters - incoming word divided by letters
    syllable_params - list, include:
                                   [0] - current syllable
                                   [1] - previous_syllable
                                   [2] - index of current syllable in word
                                   [3] - number of syllables in word
                                   [4] - how often this set of parameters
                                         of syllable is postponed
    counted_idex_table - table include syllable_params[4] element
word by syllable conditions:
                            first condition: v|v,
                            second condition: v|cv,
                            third condition: vc|c...cv,
                            where v - vowel, c - consonant
'''


# function makes a syllable from letters
def obtain_syllable(letter_number, current_letter_number,
                    word_by_letters, third_condition=False):
    syllable = ''
    sign = ['ь', 'ъ']
    if third_condition:
        for current_letter_number_temp in range(letter_number, current_letter_number + 2):
            syllable += word_by_letters[current_letter_number_temp]
        if word_by_letters[current_letter_number + 2] in sign:
            syllable += word_by_letters[current_letter_number + 2]
    else:
        for current_letter_number_temp in range(letter_number, current_letter_number + 1):
            syllable += word_by_letters[current_letter_number_temp]
            if word_by_letters[current_letter_number + 1] in sign:
                syllable += word_by_letters[current_letter_number + 1]
    return syllable


# functions records new syllable into container
def record_of_syllable(letter_number, current_letter_number, word_by_letters,
                       word, word_by_syllables, third_condition=False):
    syllable = obtain_syllable(letter_number, current_letter_number,
                               word_by_letters, third_condition)
    word += syllable
    letter_number = len(word)
    word_by_syllables.append(syllable)
    return letter_number, current_letter_number, word_by_syllables, word


# function handles last letters
def last_letters_handler(letter_number, word_by_letters,
                         word_by_syllables, vowel):
    for current_letter_number in range(letter_number, len(word_by_letters) -2):
            word_by_syllables[-1] += word_by_letters[current_letter_number]
    return word_by_syllables


# function splits input word into syllables
def get_word_by_syllable(word_incoming,word_by_syllables=[],
                         letter_number=0, word=''):
    # this is needs for correct splits
    word_by_letters = list(word_incoming) + ['а', 'б']
    if '-' in word_by_letters:
        return None
    else:
        vowel = ['а', 'у', 'о', 'ы', 'и', 'э', 'я', 'ю', 'ё', 'е']
        for current_letter_number in range(0, len(word_by_letters) - 2):
            if word_by_letters[current_letter_number] in vowel and \
               word_by_letters[current_letter_number + 1] in vowel:
                letter_number, current_letter_number , word_by_syllables, word = \
                record_of_syllable(letter_number, current_letter_number, word_by_letters,
                                      word, word_by_syllables)

            elif  word_by_letters[current_letter_number] in vowel and \
                  word_by_letters[current_letter_number + 1] not in vowel and \
                  word_by_letters[current_letter_number + 2] in vowel:
                letter_number, current_letter_number , word_by_syllables, word = \
                record_of_syllable(letter_number, current_letter_number, word_by_letters,
                                      word, word_by_syllables)

            elif word_by_letters[current_letter_number] in vowel and \
                 word_by_letters[current_letter_number + 1] not in vowel and \
                 word_by_letters[current_letter_number + 2] not in vowel:
                letter_number, current_letter_number , word_by_syllables, word = \
                record_of_syllable(letter_number, current_letter_number, word_by_letters,
                                      word, word_by_syllables, third_condition=True)
        word_by_syllables = last_letters_handler(letter_number, word_by_letters,
                                                     word_by_syllables, vowel)
        return word_by_syllables


# function obtaining parametrs of syllable(see the top)
# word_by_syllables = 'привет'
# return [('при', 'BEG', 0, 2), ('вет', 'при', 1, 2)]
def obtain_syllable_parameters(word_by_syllables):
    syllable_params = []
    if word_by_syllables:
        for syllable in word_by_syllables:
            previous_syllable = word_by_syllables[word_by_syllables.index(syllable) - 1] \
            if word_by_syllables.index(syllable) > 0 else 'BEG'
            syllable_params.append((syllable, previous_syllable,
                                   word_by_syllables.index(syllable),
                                   len(word_by_syllables)))
        return syllable_params


# function reads words from dictionary and makes list of syllables
def get_syllable_list(file_read):
    with open(file_read, 'r', encoding='utf-8') as f:
        syllable_list = []
        fields = ['word', 'PoS', 'Freq', 'R', 'D', 'Doc']
        reader = csv.DictReader(f, fields, delimiter='	')
        print('loading dictionary')
        for row in reader:
            try:
                syllable_params = []
                if list(row.get('word'))[0] != list(row.get('word'))[0].upper():
                    word_by_syllable = get_word_by_syllable(row.get('word'), [])
                    syllable_params = obtain_syllable_parameters(word_by_syllable)
                    if syllable_params:
                        syllable_list += syllable_params
            except IndexError:
                nothing_to_do = True # exceptions occurs when no vowel in word
    return syllable_list


# function makes freq table of syllables
def  get_index_table(syllable_list):
    raw_index_table = Counter(syllable_list)
    counted_idex_table = []
    for syllable_params in raw_index_table:
        temp = list(syllable_params)
        temp.append(raw_index_table[syllable_params])
        counted_idex_table.append(temp)
    return counted_idex_table


# function is generate pseudo-russian words
def pseudo_word_generator(counted_index_table):
    print('\nВас приветствует генератор псевдо русских слов!')
    while True:
        pseudo_word = ''
        number_of_syllables = input('Введите число слогов в слове или exit для выхода.\n> ')
        if number_of_syllables =='exit':
            break
        try:
            top_percent = float(input('Ведите число для отбора первых U% слогов. (Например: 20).\n> '))*0.01
            previous_syllable = 'BEG'
            for syllable_index in range(0, int(number_of_syllables)):
                syllable_list = []
                for syllable_params in counted_index_table:
                    if syllable_params[1] == previous_syllable and \
                       syllable_params[2] == syllable_index and \
                       syllable_params[3] == int(number_of_syllables):
                        syllable_list.append(syllable_params)
                syllable_list.sort(key=lambda syllable_temp: syllable_temp[-1], reverse=True)
                top_syllables = syllable_list[:int(len(syllable_list)*top_percent)]
                syllable = ''
                selected_syllable = top_syllables[random.randint(0, len(top_syllables) - 1)]
                syllable = selected_syllable[0]
                pseudo_word += syllable
                previous_syllable = syllable
        except ValueError: #exceptions occurs when len(top_syllables) == 1
            print('Попробуте ещё раз. Можно уменьшить число слогов или увеличить число для отбора первых слогов.')
        print(pseudo_word)


if __name__ == '__main__':
    pseudo_word_generator(get_index_table(get_syllable_list('freqrnc2011.csv')))
