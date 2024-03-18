from django.urls import path
from .views import *


urlpatterns = [
    path('register/', register),
    path('auth/', auth),
    path('logout/', logout_view),
    path('add/', add_song),
    path('create_playlist/', create_playlist),
    path('add_to_pl/', add_to_playlist),
    path('reaction_counter/', change_reaction_counter),
    path('', main),
    path('<int:page>/', main),
    path('<str:query>/', main),
    path('<str:query>/<int:page>/', main),
    path('genres/<str:genr>/', main),
    path('genres/<str:genr>/<int:page>/', main),
    path('<str:query>/song_<int:song_id>/', main),
    path('<str:query>/song_<int:song_id>/<int:page>/', main),
    path('<str:query>/<str:playlist>/', main),
    path('<str:query>/<str:playlist>/<int:page>/', main),
]
