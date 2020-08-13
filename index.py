import matplotlib.pyplot as plot
import pandas as pd
from SentimentAnalysis import get_emotion
from SpotipyRequests import SpotipyRequests
from GeniusRequests import get_song_lyrics
from Data import clean_data_sentiment_analysis, clear_cache, clean_data, read_data
from WordCloudRequests import create_word_cloud


# retrieves lyrics from the user's top 50 songs and first 9 playlists and returns a clean dataset of all the words
# this saves your data to a text file called output.txt so you don't need to retrieve this data every time you run
# the application!
def retrieve_spotify_data():
    sp = SpotipyRequests()

    top_tracks = sp.get_user_top_tracks(limit=50)
    playlists = []

    for i in range(8):
        playlist = sp.get_user_playlist(offset=i)
        playlists.append(playlist)

    dataset = ""
    file_object = open('songs.txt', 'a')

    for idx, item in enumerate(top_tracks['items']):
        artist = item["artists"][0]["name"]
        song_name = item['name']
        file_object.write(song_name + " - " + artist + "\n")
        dataset += get_song_lyrics(song_name, artist)

    for playlist in playlists:
        for item in playlist['tracks']['items']:
            artist = item["track"]["artists"][0]["name"]
            song_name = item["track"]['name']
            file_object.write(song_name + " - " + artist + "\n")
            dataset += get_song_lyrics(song_name, artist)

    words = clean_data(dataset)
    file_object.close()

    with open("output.txt", "w") as txt_file:
        for line in words:
            txt_file.write("".join(line) + "\n")

    return words


# ** this is here so you can read in your data from a previous run
# words = read_data("ENTER URL HERE")

words = retrieve_spotify_data()

# calculates frequency of each word in the dataset
array = {'words': {}}
lyricsArray = {}
for name in words:
    name.strip()
    if name in lyricsArray:
        lyricsArray[name]["freq"] = lyricsArray[name]["freq"] + 1
    else:
        lyricsArray[name] = {"freq": 1.0}

array['words'] = lyricsArray

# creates a pandas data frame and plots the data on a bar graph
df = pd.DataFrame(data=array['words'])
df = df.T
df = df.sort_values(by='freq', ascending=False)
df2 = df.head(35)
df2.plot.barh(title="Most frequent words used in music")
plot.show()

create_word_cloud(" ".join(words), "spotify.jpg")
clear_cache()
