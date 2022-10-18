import datetime
import pprint
import random
import spotipy
from spotipy.oauth2 import SpotifyOAuth


def main(sp: any):
    scopes = ["playlist-modify-private", "user-top-read"]

    minutes_25 = 1500000
    minutes_5 = 300000
    minutes_half = 30000

    user_id = sp.me()['id']

    artist_ids = []

    print("**seed_artists**")
    top_artists_1 = sp.current_user_top_artists(
        limit=3, time_range="short_term")
    for artist in top_artists_1["items"]:
        pprint.pprint(artist["name"])
        artist_ids.append(artist["id"])

    top_artists_2 = sp.current_user_top_artists(
        limit=1, time_range="medium_term")
    for artist in top_artists_2["items"]:
        pprint.pprint(artist["name"])
        artist_ids.append(artist["id"])

    top_artists_3 = sp.current_user_top_artists(
        limit=1, time_range="long_term")
    for artist in top_artists_3["items"]:
        pprint.pprint(artist["name"])
        artist_ids.append(artist["id"])

    recommends_upper = sp.recommendations(
        seed_artists=artist_ids, country="jp", limit=100, min_tempo=100, max_duration_ms=(minutes_5+minutes_half))

    recommends_slower = sp.recommendations(
        seed_artists=artist_ids, country="jp", limit=1, max_tempo=99, max_duration_ms=(minutes_5 + minutes_half), min_duration_ms=(minutes_5 - minutes_half))

    current_tracks = []
    current_seconds = 0

    while current_seconds <= (minutes_25 - minutes_half):
        choiced = random.choice(recommends_upper["tracks"])
        # pprint.pprint(choiced["name"])
        current_seconds += choiced["duration_ms"]
        current_tracks.append(choiced["id"])

    current_tracks.append(recommends_slower["tracks"][0]["id"])

    dt_now = datetime.datetime.now()
    timestr = dt_now.strftime('%Y-%m-%d %H:%M:%S')
    playlist = sp.user_playlist_create(
        user_id, name=f"Pomodoro Session @{timestr}", public=False, collaborative=False, description=f"")

    playlist_id = playlist["id"]

    for current_track in current_tracks:

        sp.playlist_add_items(
            playlist_id=playlist_id, items=[current_track])


if __name__ == '__main__':
    main()
