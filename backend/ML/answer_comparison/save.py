import nltk
import os
import gensim.downloader as api

word2vec_path = os.path.join(
    os.path.dirname(__file__), api.load("word2vec-google-news-300", return_path=True)
)

stopwords_list = nltk.corpus.stopwords.words("english")

stopwords_file_path = os.path.join(os.path.dirname(__file__), "stopwords.txt")

with open(stopwords_file_path, "w") as file:
    for word in stopwords_list:
        file.write(word + "\n")