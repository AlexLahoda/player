from django import forms
from django.contrib.auth.models import User
from .models import Song, Playlist

class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['title', 'author', 'year', 'genre',
                   'image', 'audio','description']
        

class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ['title',]