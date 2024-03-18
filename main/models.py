from django.db import models
from django.contrib.auth.models import User

genres = [('pop','pop'), ('club','club'), ('шансон','шансон'), ('rap','rap'),('rock','rock'), ('trance','trance'), ('dance','dance'),
        ('relax','relax'), ('dubstep','dubstep'), ('house','house'), ('metal','metal'), ('classic','classic'), ('rnb','rnb'),
        ('electric','electric'), ('instrumental','instrumental'), ('jazz','jazz'), ('blues','blues'), ('acustic','acustic'),
        ('techno','techno'), ('drum-n-base','drum-n-base'), ('alternative','alternative'), ('ethnic','ethnic'), ('indi','indi'),
        ('reggi','reggi'), ('soundtrack','soundtrack'), ('k-pop','k-pop'), ('hardstyle','hardstyle'), ('swing','swing'), ('old funk','old funk'),
        ('ska','ska'), ('eurodance','eurodance'), ('darkwave','darkwave'), ('country','country'), ('nu disco','nu disco'), ('synthwave','synthwave'),
        ('edm','edm'),('italo disco', 'italo disco'), ('breakbeat','breakbeat'), ('screamo','screamo'), ('vaporwave','vaporwave'), ('8-bit','8-bit'),
        ('noise','noise'), ('acid','acid'), ('lo-fi','lo-fi'), ('trip-hop','trip-hop'), ('electropop','electropop'), ('reggaeton','reggaeton'), 
        ('guitar gloom','guitar gloom'), ('romances','romances'), ('folk', 'folk')]


class Song(models.Model):
    title = models.CharField(max_length=64)
    author = models.CharField(max_length=64)
    year = models.DateField(default='0000-00-00')
    genre = models.CharField(max_length=64, choices=genres)
    image = models.ImageField(upload_to='main/images')
    audio = models.FileField(upload_to='main/songs')
    counter = models.PositiveIntegerField(default=0)
    uploaded_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    description = models.TextField()
    likes = models.ManyToManyField(User, related_name='likes')

    def __str__(self):
        return self.title


class Playlist(models.Model):
    title = models.CharField(max_length=64)
    songs = models.ManyToManyField(Song, related_name='songs')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
