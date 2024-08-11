import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json

from settings import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIFY_PLAYLIST_ID

spotify = spotipy.Spotify(
    client_credentials_manager=SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID,
                                                        client_secret=SPOTIPY_CLIENT_SECRET))

tracks = {}
for offset in range(0, 1301, 100):
    results = spotify.playlist_items(playlist_id=SPOTIFY_PLAYLIST_ID, offset=offset)
    for track in results["items"]:
        tracks[track["track"]["name"]] = {"duration_ms": track["track"]["duration_ms"],
                                          "artists": [artist["name"] for artist in track["track"]["artists"]]}

print(tracks)
print(len(tracks))
json.dump(tracks, open("songs_from_spotify_playlist.json", "w"))
