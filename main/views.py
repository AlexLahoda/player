from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth.models import User
import re
import json
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .models import Song, genres, Playlist
from .forms  import SongForm, PlaylistForm
from django.http import JsonResponse
from music_player.settings import BOT, ADMIN_CHAT_ID
from django.template.loader import render_to_string
import os


def register(request: HttpRequest):
    if not request.user.is_authenticated:
        context = {}
        if request.method == 'POST':
            email = request.POST.get('email')
            name = request.POST.get('name')
            surname = request.POST.get('surname')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            context['email'] = email
            context['name'] = name
            context['surname'] = surname

            if email and name and surname and password and confirm_password:  
                if re.fullmatch(r'[\w!-]+@.\w+.\w+', email):
                    if len(password) > 7:
                        if password == confirm_password:
                            try:
                                user = User.objects.create_user(username=email,
                                                        first_name=name,
                                                        last_name=surname,
                                                            password=password)
                                login(request, user)
                                return redirect('/')
                            except IntegrityError:
                                context['error'] = "Користувач з таким email вже існує"
                        else:
                            context['error'] = 'Паролі не співпадають'
                    else:
                        context['error'] = 'Довжина паролю повинна бути більше 8 символів'
                else:
                    context['error'] = 'Неправильний формат email'
            else:
                context['error'] = 'Заповніть всі поля'
        return render(request, 'main/reg.html', context)
    return redirect('/')

def auth(request: HttpRequest):
    if not request.user.is_authenticated:
        context = {}
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')

            context['email'] = email

            if email and password:
                user = authenticate(username=email, password=password)
                if user:
                    login(request, user)
                    return redirect('/')
            else:
                context['error'] = 'Логін чи пароль введені неправлильно'
        return render(request, 'main/auth.html', context)
    return redirect('/')

def main(request: HttpRequest, page=1, query=None, song_id=None, genr=None, playlist=None):
    song = None
    pages_iter = None
    first_page = None
    pages_qty = None
    playlists = None
    in_playlist = 'no'
    form_genres = [i[0] for i in genres]
    search = request.GET.get('data')
    songs = Song.objects.all()
    if search:
        songs =songs.filter(title__icontains=search) or songs.filter(author__icontains=search)
    if genr:
        songs = songs.filter(genre=genr)
    if query:
        if query == 'favorite':
            songs = request.user.likes.all()
        elif query =='uploaded_by':
            song=Song.objects.get(id=song_id)
            songs = songs.filter(uploaded_by=song.uploaded_by)
        elif query == 'playlists':
            playlist=Playlist.objects.get(title=playlist)
            songs=playlist.songs.all()
    if request.user.is_authenticated:
        playlists = Playlist.objects.filter(created_by=request.user) 
    if songs:
        song_qty = songs.count()
        ipp=5
        start = (page - 1) * ipp
        end = start + ipp
        songs = songs[start:end]
        pages_qty = song_qty//ipp + 1 if song_qty%ipp else song_qty//ipp
        if pages_qty>1:
            pages_iter = range(1 if page-5 < 1 else page-5,pages_qty+1 if page+6 > pages_qty+1 else page + 6)
        first_page = request.get_full_path()
        first_page = re.match(r'/([a-zA-Z_]+[0-9]*/)*',first_page).group()
    if re.match(r'/playlists/\w+/', request.get_full_path()):
        in_playlist = 'yes'
    context = {
        'songs': songs,
        'song':song,
        'genres':form_genres,
        'pages_iter': pages_iter,
        'first_page': first_page,
        'last_page': pages_qty,
        'playlists': playlists,
        'in_playlist': in_playlist
    }
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = {
            'songs': render_to_string('main/song_list1.html', {'songs': songs, 'pages_iter': pages_iter, 'first_page': first_page,'last_page': pages_qty, 'playlists': playlists, 'in_playlist': in_playlist, 'user': request.user}),
            'song': render_to_string('main/song.html',{'song': song,}),
        }
        return JsonResponse(data)
    
    return render(request, 'main/main1.html', context)

def change_reaction_counter(request: HttpRequest):
    if request.method == 'POST':
        song_id = request.POST.get('song_id')
        song = Song.objects.get(id=song_id)
        if request.user.is_authenticated:
            if request.POST.get('action') == 'add':
                song.likes.add(request.user)
            elif request.POST.get('action') == 'remove':
                song.likes.remove(request.user)
            elif request.POST.get('action') == 'del' and request.user == song.uploaded_by:
                route = str(song.audio.path)
                song.delete()
                if os.path.exists(route):
                    os.remove(route)
                    print("Deleted")
                else:
                    print("Not found")
        if request.POST.get('action') == 'count':
            song.counter +=1
            song.save()
            return JsonResponse({'counter': song.counter})
    return render(request, 'main/main1.html')

def logout_view(request: HttpRequest):
    logout(request)
    return redirect('/')

def create_playlist(request: HttpRequest):
    if request.user.is_authenticated:
        form = PlaylistForm(request.POST or None)
        if form.is_valid() and request.method=='POST':
            Playlist.objects.create(
            title=form.data.get('title'),
            created_by=request.user,
        )
        context = {
                'form': form,
            }
        return render(request, 'main/create_playlist.html', context)
    return redirect('/')

def add_song(request: HttpRequest):
    if request.user.is_authenticated:
        form = SongForm(request.POST or None, request.FILES or None)
        if form.is_valid() and request.method=='POST':
            Song.objects.create(
            title=form.data.get('title'),
            author=form.data.get('author'),
            year=form.data.get('year'),
            genre=form.data.get('genre'),
            image=request.FILES['image'],
            audio=request.FILES['audio'],
            counter=0,
            uploaded_by=request.user,
            description=form.data.get('description')
        )
            BOT.send_message(ADMIN_CHAT_ID, 
f"Додана нова композиція від {request.user}:\n{form.data.get('title')} - {form.data.get('author')}")
        context = {
                'form': form,
            }
        return render(request, 'main/add_song.html', context)
    return redirect('/')

def add_to_playlist(request: HttpRequest):
    if request.user.is_authenticated:
        if request.method == "POST":
            if request.POST.get('action') == 'add_pl':
                playlists = json.loads(request.POST.get('playlists'))
                song = Song.objects.get(id=request.POST.get('song_id'))
                if playlists:
                    for playlist in playlists:
                        playlist = Playlist.objects.get(id=playlist)
                        playlist.songs.add(song)
            elif request.POST.get('action') == 'del_pl':
                playlist = re.findall(r'/playlists/[0-9A-Za-z_]+/', request.POST.get('path'))[0]
                playlist = playlist.split('/')[2]
                playlist = Playlist.objects.get(title=playlist)
                if playlist.created_by == request.user:
                    song = Song.objects.get(id=request.POST.get('song_id'))
                    playlist.songs.remove(song)
    return render(request, 'main/main1.html')

