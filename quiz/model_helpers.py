from django.db.models import Count, Q
from .models import *
from random import shuffle, randint


def get_random_text(past_ids):
    got_text = False
    i = 0
    while not got_text:
        # Select a random language with more at least 1 text samples
        possible_languages = Language.objects.annotate(texts=Count('textsample')).filter(texts__gt=0)
        possible_languages = list(possible_languages)
        shuffle(possible_languages)  # Because order_by('?') turns this into a list where one language can appear several times, once per text (wtf)
        language = possible_languages[0]

        # Tries to find a text that hasn't already been used (max 10 attempts)
        texts = TextSample.objects.filter(language=language).exclude(pk__in=past_ids).order_by('?')
        if len(texts) > 0:
            got_text = True
        i = i + 1
        # If 10 attempts have failed, return a text anyway, even if it has already been used
        if i >= 10:
            return TextSample.objects.filter(language=language).order_by('?')[0]
    return texts[0]


def get_random_song(past_ids):
    got_song = False
    i = 0
    while not got_song:
        # Select a random language with more at least 1 song
        min_songs = randint(0, 4) # To avoid getting the same song too often with languages that have only 1 or 2
        possible_languages = Language.objects.annotate(songs=Count('song')).filter(songs__gt=min_songs)
        possible_languages = list(possible_languages)
        shuffle(possible_languages)  # Because order_by('?') turns this into a list where one language can appear several times, once per song (wtf)
        language = possible_languages[0]

        # Tries to find a song that hasn't already been used (max 10 attempts)
        songs = Song.objects.filter(language=language).exclude(pk__in=past_ids).order_by('?')
        if len(songs) > 0:
            got_song = True
        i = i + 1
        # If 10 attempts have failed, return a song anyway, even if it has already been used
        if i >= 10:
            return Song.objects.filter(language=language).order_by('?')[0]
        if i > 1:
            print("Attempt " + str(i))
    return songs[0]


def get_language_choices(language, number, difficult=False, spoken=False):
    incompatible_codes = [language.code]
    incompatible_languages = language.incompatible_spoken_languages.all() if spoken else language.incompatible_written_languages.all()
    for l in incompatible_languages:
        incompatible_codes.append(l.code)

    if difficult:  # Choose languages within the same categories
        other_languages = Language.objects.none()
        for category in language.categories.all():
            other_languages = other_languages | category.language_set.all()
        other_languages = other_languages.exclude(code__in=incompatible_codes).distinct()
        other_languages = list(other_languages)  # Necessary because distinct() + order_by('?') = doesn't work
        shuffle(other_languages)
        if number >= 8:  # To add a couple random languages
            other_languages = other_languages[:number-2]
        else:
            other_languages = other_languages[:number-1]

        # If not enough languages in the same categories, add random languages
        if len(other_languages) < number - 1:
            missing = number - len(other_languages)
            for l in other_languages:
                incompatible_codes.append(l.code)
            other_languages = other_languages + list(Language.objects.exclude(code__in=incompatible_codes).order_by('?')[0:missing-1])
    else:
        other_languages = Language.objects.exclude(code__in=incompatible_codes).order_by('?')[:number-1]
    result = list(other_languages)  # Necessary to avoid weird results (otherwise the query is apparently reevaluated)
    result.append(language)
    result.sort(key=lambda l: l.name)

    languages = {}
    for lang in result:
        languages[lang.code] = lang.name
    return languages


def played_text(id, correct):
    text = TextSample.objects.get(pk=id)
    text.times_played += 1
    if correct:
        text.correctly_answered += 1
    text.save()


def played_song(id, correct):
    song = Song.objects.get(pk=id)
    song.times_played += 1
    if correct:
        song.correctly_answered += 1
    song.save()


def update_song_error_reports(id):
    song = Song.objects.get(pk=id)
    song.error_reports += 1
    song.save()
