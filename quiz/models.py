from django.db import models
from django.utils import translation


class Language(models.Model):
    DIRECTION_LTR = 'ltr'
    DIRECTION_RTL = 'rtl'
    DIRECTION_CHOICES = [
        (DIRECTION_LTR, 'Left to right →'),
        (DIRECTION_RTL, 'Right to left ←'),
    ]

    code = models.CharField(primary_key=True,
                            max_length=3,
                            help_text="ISO 639-1 or ISO 639-2 code")
    name = models.CharField(max_length=60,
                               unique=True)
    direction = models.CharField(max_length=3,
                                 choices=DIRECTION_CHOICES,
                                 default=DIRECTION_LTR)
    categories = models.ManyToManyField('Category',
                                        blank=True)
    incompatible_spoken_languages = models.ManyToManyField('self',
                                                           blank=True,
                                                           help_text="Languages that are too similar to be distinguished when spoken (e.g. Hindi and Urdu)")
    incompatible_written_languages = models.ManyToManyField('self',
                                                            blank=True,
                                                            help_text="Languages that are too similar to be distinguished in writing (e.g. Malay and Indonesian)")

    def __str__(self):
        return "{} ({})".format(self.name, self.code)

    def align(self):
        return "left" if self.direction == self.DIRECTION_LTR else "right"


class TextSample(models.Model):
    text = models.TextField()
    language = models.ForeignKey('Language',
                                 on_delete=models.CASCADE)
    source = models.URLField(blank=True,
                             null=True,
                             max_length=255)
    license = models.ForeignKey('License',
                                on_delete=models.SET_NULL,
                                null=True,
                                blank=True,
                                help_text="License under which the text is published")
    times_played = models.IntegerField(default=0)
    correctly_answered = models.IntegerField(default=0)

    def __str__(self):
        return self.text[0:30] + "…"

    def truncated_source(self):
        if len(self.source) > 75:
            return self.source[0:70] + "…"
        else:
            return self.source


class License(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField(blank=True,
                          null=True)

    def __str__(self):
        return self.name


class Song(models.Model):
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200,
                              blank=True,
                              null=True)
    language = models.ForeignKey('Language',
                                 on_delete=models.CASCADE)
    youtube_url = models.URLField(unique=True)
    start_at = models.IntegerField(default=0,
                                   help_text="Number of seconds where the video should start")
    times_played = models.IntegerField(default=0)
    correctly_answered = models.IntegerField(default=0)
    error_reports = models.IntegerField(default=0, help_text="Number of times a player reported that the video does not work")

    def __str__(self):
        if self.artist is None or self.artist == "":
            return self.title
        else:
            return "{} – {}".format(self.artist, self.title)

    def embed_url(self):
        url = self.youtube_url.replace('watch?v=', 'embed/') + "?autoplay=1"
        if self.start_at > 0:
            url = url + "&start=" + str(self.start_at)
        return url


# Categories of related or "similar" languages
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"
