import os

# removes stop words and extra characters from a string and formats the string into an array of words
def clean_data(string):
    string = string.lower()

    string = string.replace(r"(http|@)\S+", "")
    string = string.replace(r"’", "'")
    string = string.replace(r"[^a-z\':_]", "")
    string = string.replace("\n", ' ')
    string = string.replace('\u2005', ' ')
    string = string.replace('•', ' ')

    stop_chars = ['(', ')', '&', '\'', '\"', ',', '[', ']', ':', '—', '-', '1', '2', '3', '4', '5',
                  '6', '7', '8', '9', '0', '.', '/', '?']
    for char in stop_chars:
        string = string.replace(char, "")

    file = open('stop-words.txt', 'r')
    stopwords = []
    for line in file.readlines():
        stopwords.append(line.strip())

    words = []
    for word in string.split():
        if word not in stopwords:
            words.append(word)

    return words


# removes cached spotify access keys
def clear_cache():
    file_list = [f for f in os.listdir("./caches")]
    for f in file_list:
        os.remove(os.path.join("./caches", f))

# removes stop words and extra characters from a string and formats the string into an array of words for
# sentiment analysis
def clean_data_sentiment_analysis(string):
    string = string.lower()

    stop_chars = ['(', ')', '&', '\'', '\"', ',', '[', ']', ':', '—', '-', '1', '2', '3', '4', '5',
                  '6', '7', '8', '9', '0', '.', '/', 'na']
    for char in stop_chars:
        string = string.replace(char, "")

    file = open('stop-words-sentiment.txt', 'r')
    stopwords = []
    for line in file.readlines():
        stopwords.append(line.strip())

    sentences = []
    for sentence in string.split("\n"):
        words = sentence.split()
        final_string = ''

        for word in words:
            if word not in stopwords:
                final_string = final_string + " " + word

        if final_string != '':
            sentences.append(final_string.strip())

    return sentences

# reads data from a text file and returns array
def read_data(url):
    file = open(url, 'r')
    words = []
    for line in file.readlines():
        words.append(line.strip())
    return words
