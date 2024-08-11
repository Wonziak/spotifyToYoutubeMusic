import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from ytmusicapi import YTMusic

from settings import SKIP_SPOTIFY, SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIFY_PLAYLIST_ID, YOUTUBE_PLAYLIST_ID, \
    duration_difference


def create_json_from_spotify_playslist(spotify_playlist_id: str = SPOTIFY_PLAYLIST_ID) -> None:
    """
    This function reads songs from Spotify playlist and saves song titles, artists and duration in miliseconds in file:
    songs_from_spotify_playlist.json.

    :param spotify_playlist_id: Spotify playlist it to reads songs from
    :return: None
    """
    spotify = spotipy.Spotify(
        client_credentials_manager=SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID,
                                                            client_secret=SPOTIPY_CLIENT_SECRET))

    tracks = {}
    for offset in range(0, 1301, 100):
        results = spotify.playlist_items(playlist_id=spotify_playlist_id, offset=offset)
        for track in results["items"]:
            tracks[track["track"]["name"]] = {"duration_ms": track["track"]["duration_ms"],
                                              "artists": [artist["name"] for artist in track["track"]["artists"]]}

    json.dump(tracks, open("songs_from_spotify_playlist.json", "w"))
    print("JSON file with Spotify songs from playlist ")


def search_for_songs_in_ytmusic_and_add_to_playlist(youtube_playlist_id: str = YOUTUBE_PLAYLIST_ID,
                                                    duration_difference: int = duration_difference) -> None:
    """
    This function searches for song in Youtube music, compares duration to Spotify duration and adds song to playlist.
    :param youtube_playlist_id: Youtube Music playlist id
    :param duration_difference: difference of duration in Youtube compared to Spotify
    :return: None
    """
    json_file = open("songs_from_spotify_playlist.json")
    tracks = json.load(json_file)

    yt = YTMusic('oauth.json')

    for title, data in tracks.items():
        artists = " ".join(data['artists'])
        search_results = yt.search(f"{title} {artists}")
        try:
            duration_seconds_youtube = search_results[0]["duration_seconds"]
            duration_seconds_spotify = data["duration_ms"] / 1000
            if duration_seconds_spotify - duration_difference <= duration_seconds_youtube <= duration_seconds_spotify + duration_difference:
                yt.add_playlist_items(youtube_playlist_id, [search_results[0]['videoId']])
                print(search_results[0]["title"])
            else:
                print(f"Song '{title}' with similar duration to Spotify not found")
                with open("missing_songs.txt", "a") as file:
                    file.write(title + "\n")
        except KeyError:
            print(f"Song '{title}' not found in youtube music")
            with open("missing_songs.txt", "a") as file:
                file.write(title + "\n")
    print("All songs checked and added")


if __name__ == "__main__":
    """
    You can skip creating JSON from Spotify playlist if it was already created and you dont want to recreate it.
    """
    if not SKIP_SPOTIFY:
        create_json_from_spotify_playslist()
    search_for_songs_in_ytmusic_and_add_to_playlist(youtube_playlist_id=YOUTUBE_PLAYLIST_ID,
                                                    duration_difference=duration_difference)
