## Spotify playlist to Youtube Music playlist converter

### Getting started

Run `pip install -r requirements.txt`

Follow steps from: [Authenticating with the Spotipy API](https://www.youtube.com/watch?v=kaBVN8uP358) to create Spotify app.

Then set your credentials and your spotify playlist id in `settings.py`

To get playlist id, you can copy its link from `Share` in UI, and copy `<playlist_id>` part `/playlist/<playlist_id>`

Before you run this program create playlist in Youtube Music and get its ID like you did for Spotify playlist -
`playlist?list=<playlist_id` and set it in `settings.py`

To make Youtube Music work, you need to run `ytmusicapi oauth`  and follow instructions from terminal -
Youtube music does not have any API. It will generate `oauth.json` file needed for it to work.

### Error handling
Program will generate file `missing_songs.txt`. That contains titles of songs that have different duration than Spotify version -
by default it is +/- 10 seconds, but can be configurable by `duration_difference` parameter in `settings.py`.  
Also, this file containes titles of songs that for some reason could not be found in Youtube Music and should be added manually.

### It looks like Youtube API sometimes crashes so this program may require restarts, especially if your playlist is long. Regenerating token with `ytmusicapi oauth` should help.

## Results.
For my playlist, that contains 1120 songs, this program missed 100.