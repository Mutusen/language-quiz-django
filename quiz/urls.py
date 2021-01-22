from django.urls import path
from . import views

urlpatterns = [
    path('wikipedia/<str:user_language>/<str:language_code>/', views.wikipedia, name="wikipedia"),
    path('getcount/', views.getcount, name="getcount"),
    path('textquestion/', views.textquestion, name="textquestion"),
    path('songquestion/', views.songquestion, name="songquestion"),
    path('update-text-stats/', views.update_text_stats, name="update_text_stats"),
    path('update-song-stats/', views.update_song_stats, name="update_song_stats"),
    path('report-broken-video/', views.report_broken_video, name="report_broken_video"),
]

