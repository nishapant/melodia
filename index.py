import matplotlib.pyplot as plot
import pandas as pd
from SentimentAnalysis import get_emotion
from SpotipyRequests import SpotipyRequests
from GeniusRequests import get_song_lyrics
from Data import clean_data_sentiment_analysis, clear_cache, clean_data, read_data
from WordCloudRequests import create_word_cloud


# retrieves lyrics from the user's top 50 songs and first 9 playlists and returns a clean dataset of all the words
# this saves your data to a text file called output.txt so you don't need to retrieve this data every time you run
# the application! pass in a boolean value of whether or not you are doing sentiment analysis with this dataset
def retrieve_spotify_data(sentiment_analysis):
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
        # file_object.write(song_name + " - " + artist + "\n")
        dataset += get_song_lyrics(song_name, artist)

    for playlist in playlists:
        for item in playlist['tracks']['items']:
            artist = item["track"]["artists"][0]["name"]
            song_name = item["track"]['name']
            # file_object.write(song_name + " - " + artist + "\n")
            dataset += get_song_lyrics(song_name, artist)
    words = clean_data_sentiment_analysis(dataset) if sentiment_analysis else clean_data(dataset)

    file_object.close()

    with open("output.txt", "w") as txt_file:
        for line in words:
            txt_file.write("".join(line) + "\n")

    return words


# ** this is here so you can read in your data from a previous run
# words = read_data("output.txt")

words = retrieve_spotify_data(False)

words_sentiment = retrieve_spotify_data(True)

# will retrieve the overall emotions from the songs in the dataset
emotions = get_emotion(" ".join(words_sentiment))

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
df_freq = pd.DataFrame(data=array['words'])
df_freq = df_freq.T
df_freq = df_freq.sort_values(by='freq', ascending=False)
df_freq_plot = df_freq.head(35)
df_freq_plot.plot.barh(title="Most frequent words used songs")
plot.show()

# creates a wordcloud in the shape of the jpg specified with the data from words
create_word_cloud(" ".join(words), "recordPlayer.jpg")

# creates a pie chart of the levels of emotions within the data from emotions
colors = ['#441151', '#454ADE', '#386150', '#9FA2B2', '#9CD08F', '#145C9E']
new_dataframe = {'emotions': [], 'values': []}
for i in emotions:
    new_dataframe['emotions'].append(i)
    new_dataframe['values'].append(emotions[i])

df_emotions = pd.DataFrame(data=new_dataframe, index=new_dataframe['emotions'])

explode = (0, 0, 0, 0.2, 0, 0)

df_emotions.plot.pie(y='values', colors=colors, figsize=(5, 5), labels=new_dataframe['values'], explode=explode,
            shadow=True)

plot.title("Sentiment analysis in songs")
plot.legend(new_dataframe['emotions'], loc=10)
plot.show()

clear_cache()
