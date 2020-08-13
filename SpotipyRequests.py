import spotipy
from spotipy.oauth2 import SpotifyOAuth


class SpotipyRequests:
    SPOTIPY_CLIENT_ID = "INSERT CLIENT ID HERE"
    SPOTIPY_CLIENT_SECRET = "INSERT CLIENT SECRET HERE"
    SPOTIPY_REDIRECT_URI = "INSERT REDERICT URI HERE"
    scope = "user-library-read user-top-read"

    sp = None

    def __init__(self):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=self.SPOTIPY_CLIENT_ID,
                                                            client_secret=self.SPOTIPY_CLIENT_SECRET,
                                                            redirect_uri=self.SPOTIPY_REDIRECT_URI,
                                                            scope=self.scope, cache_path="./caches/cache"))

    def get_user_saved_tracks(self):
        return self.sp.current_user_saved_tracks()

    def get_user_top_tracks(self, limit):
        return self.sp.current_user_top_tracks(limit=limit, time_range='medium_term', offset=0)

    def get_user_playlist(self, offset):
        playlist_id = self.sp.current_user_playlists(limit=1, offset=offset)['items'][0]['id']
        return self.sp.playlist(playlist_id)
