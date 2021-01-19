import json
from time import sleep

from django.db.models import Count
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from quiz import model_helpers
from quiz.wikipedia import get_wikipedia_link
from quiz.models import Language, TextSample, Song


def wikipedia(request, language_code):
    return redirect(get_wikipedia_link(language_code))


def getcount(request):
    texts = TextSample.objects.count()
    text_languages = Language.objects.annotate(textsamples=Count('textsample')).filter(textsamples__gt=0).count()

    songs = Song.objects.count()
    song_languages = Language.objects.annotate(songs=Count('song')).filter(songs__gt=0).count()

    response = JsonResponse({
        'texts': texts,
        'text_languages': text_languages,
        'songs': songs,
        'song_languages': song_languages,
    })
    return response


@csrf_exempt
@require_POST
def textquestion(request):
    postdata = json.loads(request.body.decode('utf-8'))
    choices = int(postdata['choices'])
    difficult = bool(postdata['difficult'])
    past_texts = []
    if postdata['pastQuestionsIds'] != "":
        ids = postdata['pastQuestionsIds'].split(",")
        for i in ids:
            past_texts.append(int(i))

    guess_text = model_helpers.get_random_text(past_texts)
    language_choices = model_helpers.get_language_choices(guess_text.language, choices, difficult)

    jsondata = {
        'id': guess_text.id,
        'correctAnswer': guess_text.language.code,
        'direction': guess_text.language.direction,
        'text': guess_text.text,
        'source': guess_text.source,
        'choices': language_choices
    }
    if guess_text.license:
        jsondata['license'] = {'name': guess_text.license.name, 'url': guess_text.license.url}

    response = JsonResponse(jsondata)
    return response


@csrf_exempt
@require_POST
def songquestion(request):
    postdata = json.loads(request.body.decode('utf-8'))
    choices = int(postdata['choices'])
    difficult = bool(postdata['difficult'])
    past_songs = []
    if postdata['pastQuestionsIds'] != "":
        ids = postdata['pastQuestionsIds'].split(",")
        for i in ids:
            past_songs.append(int(i))

    guess_song = model_helpers.get_random_song(past_songs)
    language_choices = model_helpers.get_language_choices(guess_song.language, choices, difficult)

    jsondata = {
        'id': guess_song.id,
        'correctAnswer': guess_song.language.code,
        'direction': guess_song.language.direction,
        'youtube_url': guess_song.youtube_url,
        'embed_url': guess_song.embed_url(),
        'title': guess_song.title,
        'artist': guess_song.artist,
        'choices': language_choices,
    }
    response = JsonResponse(jsondata)
    return response


@csrf_exempt
@require_POST
def update_text_stats(request):
    postdata = json.loads(request.body.decode('utf-8'))
    model_helpers.played_text(postdata['id'], postdata['correct'])
    return HttpResponse('')


@csrf_exempt
@require_POST
def update_song_stats(request):
    postdata = json.loads(request.body.decode('utf-8'))
    model_helpers.played_song(postdata['id'], postdata['correct'])
    return HttpResponse('')


@csrf_exempt
@require_POST
def report_broken_video(request):
    postdata = json.loads(request.body.decode('utf-8'))
    model_helpers.update_song_error_reports(postdata['id'])
    return HttpResponse('')
