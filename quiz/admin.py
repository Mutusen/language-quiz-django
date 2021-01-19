import csv
from django.contrib import admin
from django import forms
from django.db.models import Count
from django.shortcuts import redirect, render
from django.urls import path
from .models import *


class CsvImportForm(forms.Form):
    csv_file = forms.FileField()


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'direction', 'text_samples', 'songs', 'num_categories')
    ordering = ['name']
    search_fields = ['name', 'code']
    autocomplete_fields = ['categories', 'incompatible_spoken_languages', 'incompatible_written_languages']

    def get_queryset(self, request):
        qs = super(LanguageAdmin, self).get_queryset(request)
        qs = qs.annotate(songs=Count('song')).annotate(text_samples=Count('textsample'))
        return qs

    def text_samples(self, obj):
        return TextSample.objects.filter(language=obj).count()

    text_samples.short_description = 'Text samples'
    text_samples.admin_order_field = 'text_samples'

    def songs(self, obj):
        return Song.objects.filter(language=obj).count()

    songs.short_description = 'Songs'
    songs.admin_order_field = 'songs'

    def num_categories(self, obj):
        return obj.categories.count()

    num_categories.short_description = 'Categories'


@admin.register(TextSample)
class TextSampleAdmin(admin.ModelAdmin):
    list_display = ('language', 'short_text', 'license', 'text_length', 'url_length', 'times_played', 'correctly_answered', 'success_rate')
    autocomplete_fields = ['language', 'license']
    search_fields = ['text', 'source']
    list_editable = ('license',)
    list_filter = ['language']

    def short_text(self, obj):
        return obj.text[0:60] + ("…" if len(obj.text) > 60 else "")

    short_text.short_description = 'Sample'

    def text_length(self, obj):
        return len(obj.text)

    text_length.short_description = 'Length'

    def success_rate(self, obj):
        if obj.times_played == 0:
            return '-'
        else:
            return str(obj.correctly_answered / obj.times_played * 100) + "%"

    success_rate.short_description = 'Success rate'

    def url_length(self, obj):
        return len(obj.source)

    url_length.short_description = 'URL length'


@admin.register(License)
class LicenseAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')
    search_fields = ['name']


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'language', 'youtube_url', 'times_played', 'correctly_answered', 'success_rate', 'error_reports')
    autocomplete_fields = ['language']
    search_fields = ['title', 'artist']
    list_filter = ['language']

    change_list_template = "admin/songs_changelist.html"

    def success_rate(self, obj):
        if obj.times_played == 0:
            return '-'
        else:
            return str(obj.correctly_answered / obj.times_played * 100) + "%"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import-csv/', self.import_csv),
        ]
        return my_urls + urls

    def import_csv(self, request):
        if request.method == "POST":
            csv_file = request.FILES["csv_file"].read().decode('utf-8').splitlines()
            reader = csv.reader(csv_file)
            saved_songs = []
            for row in reader:
                if not Song.objects.filter(youtube_url__exact=row[3]).exists():
                    language = Language.objects.get(code=row[0])
                    song = Song(language=language,
                                title=row[1],
                                artist=row[2],
                                youtube_url=row[3],
                                start_at=0 if row[4] == "" else int(row[4])
                                )
                    song.save()
                    saved_songs.append(str(song))
            self.message_user(request, "Your CSV file has been imported. Saved songs ({}): {}.".format(len(saved_songs), ", ".join(saved_songs)))
            return redirect("..")
        form = CsvImportForm()
        payload = {"form": form}
        return render(
            request, "admin/csv_form.html", payload
        )


class CategoryLanguageInline(admin.TabularInline):
    model = Language.categories.through


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']
    inlines = [CategoryLanguageInline]
