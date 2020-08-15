import lyricsgenius

GENIUS_CLIENT_ACCESS_TOKEN = "INSERT CLIENT ACCESS TOKEN HERE"

genius = lyricsgenius.Genius(GENIUS_CLIENT_ACCESS_TOKEN)

# returns the lyrics from a given song and artist
def get_song_lyrics(song_name, artist):
    song = genius.search_song(song_name, artist)
    if song is not None:
        return song.lyrics
    return ""
