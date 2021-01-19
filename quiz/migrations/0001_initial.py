# Generated by Django 3.1.5 on 2021-01-19 18:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('code', models.CharField(help_text='ISO 639-1 or ISO 639-2 code', max_length=3, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=60, unique=True)),
                ('direction', models.CharField(choices=[('ltr', 'Left to right →'), ('rtl', 'Right to left ←')], default='ltr', max_length=3)),
                ('categories', models.ManyToManyField(blank=True, to='quiz.Category')),
                ('incompatible_spoken_languages', models.ManyToManyField(blank=True, help_text='Languages that are too similar to be distinguished when spoken (e.g. Hindi and Urdu)', related_name='_language_incompatible_spoken_languages_+', to='quiz.Language')),
                ('incompatible_written_languages', models.ManyToManyField(blank=True, help_text='Languages that are too similar to be distinguished in writing (e.g. Malay and Indonesian)', related_name='_language_incompatible_written_languages_+', to='quiz.Language')),
            ],
        ),
        migrations.CreateModel(
            name='License',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('url', models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TextSample',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('source', models.URLField(blank=True, max_length=255, null=True)),
                ('times_played', models.IntegerField(default=0)),
                ('correctly_answered', models.IntegerField(default=0)),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.language')),
                ('license', models.ForeignKey(blank=True, help_text='License under which the text is published', null=True, on_delete=django.db.models.deletion.SET_NULL, to='quiz.license')),
            ],
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('artist', models.CharField(blank=True, max_length=200, null=True)),
                ('youtube_url', models.URLField(unique=True)),
                ('start_at', models.IntegerField(default=0, help_text='Number of seconds where the video should start')),
                ('times_played', models.IntegerField(default=0)),
                ('correctly_answered', models.IntegerField(default=0)),
                ('error_reports', models.IntegerField(default=0, help_text='Number of times a player reported that the video does not work')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.language')),
            ],
        ),
    ]