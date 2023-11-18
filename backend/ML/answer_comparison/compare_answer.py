import nltk
import os
import numpy as np
from gensim.models.keyedvectors import KeyedVectors
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import math
import requests
from gensim import models

# nltk.download("punkt")
# nltk.download("stopwords")

word2vec = models.KeyedVectors.load_word2vec_format(
    os.path.join(
        os.path.dirname(__file__),
        "word2vec-google-news-300/word2vec-google-news-300.gz",
    ),
    binary=True,
)

stopwords_file_path = os.path.join(os.path.dirname(__file__), "stopwords.txt")

def GrammerChecker(answer):
    req = requests.get(
        "https://api.textgears.com/check.php?text=" + answer + "&key=JmcxHCCPZ7jfXLF6"
    )
    no_of_errors = len(req.json()["errors"])

    # print(no_of_errors)

    if no_of_errors > 5:
        g = 0
    else:
        g = 1
    return g


# key Word matching
def KeyWordmatching(X, Y_lst):
    # tokenization
    result = 0
    X_list = word_tokenize(X)

    # sw contains the list of stopwords
    sw = nltk.corpus.stopwords.words("english")
    l1 = []
    l2 = []

    # remove stop words from string
    X_set = {w for w in X_list if not w in sw}

    for Y in Y_lst:
        Y_list = word_tokenize(Y)
        Y_set = {w for w in Y_list if not w in sw}
        # form a set containing keywords of both strings
        rvector = X_set.union(Y_set)
        for w in rvector:
            if w in X_set:
                l1.append(1)  # create a vector
            else:
                l1.append(0)
            if w in Y_set:
                l2.append(1)
            else:
                l2.append(0)
        c = 0

        # cosine formula
        for i in range(len(rvector)):
            c += l1[i] * l2[i]
        cosine = c / float((sum(l1) * sum(l2)) ** 0.5)
        cosine = cosine * 100
        # print(cosine)
        result = result + cosine
        # print('result',result)
        # print("similarity: ", cosine)
    cosine = result / 3
    kval = 0
    if cosine > 90:
        kval = 1
    elif cosine > 80:
        kval = 2
    elif cosine > 60:
        kval = 3
    elif cosine > 40:
        kval = 4
    elif cosine > 20:
        kval = 5
    else:
        kval = 6
    return kval


# length of string
def CheckLenght(client_answer):
    client_ans = len(client_answer.split())
    # return client_ans
    kval1 = 0
    if client_ans > 50:
        kval1 = 1
    elif client_ans > 40:
        kval1 = 2
    elif client_ans > 30:
        kval1 = 3
    elif client_ans > 20:
        kval1 = 4
    elif client_ans > 10:
        kval1 = 5
    else:
        kval1 = 6
    return kval1


# Synonyam


class DocSim:
    def __init__(self, w2v_model, stopwords=None):
        self.w2v_model = w2v_model
        self.stopwords = stopwords if stopwords is not None else []

    def vectorize(self, doc: str) -> np.ndarray:
        """
        Identify the vector values for each word in the given document
        :param doc:
        :return:
        """
        doc = doc.lower()
        words = [w for w in doc.split(" ") if w not in self.stopwords]
        word_vecs = []
        for word in words:
            try:
                vec = self.w2v_model[word]
                word_vecs.append(vec)
            except KeyError:
                # Ignore, if the word doesn't exist in the vocabulary
                pass

        # Assuming that document vector is the mean of all the word vectors
        # PS: There are other & better ways to do it.
        vector = np.mean(word_vecs, axis=0)
        return vector

    def _cosine_sim(self, vecA, vecB):
        """Find the cosine similarity distance between two vectors."""
        csim = np.dot(vecA, vecB) / (np.linalg.norm(vecA) * np.linalg.norm(vecB))
        if np.isnan(np.sum(csim)):
            return 0
        return csim

    def calculate_similarity(self, source_doc, target_docs=None, threshold=0):
        """Calculates & returns similarity scores between given source document & all
        the target documents."""
        if not target_docs:
            return []

        if isinstance(target_docs, str):
            target_docs = [target_docs]

        source_vec = self.vectorize(source_doc)
        results = []
        result = []
        for doc in target_docs:
            target_vec = self.vectorize(doc)
            sim_score = self._cosine_sim(source_vec, target_vec)
            result.append(sim_score)
            if sim_score > threshold:
                results.append({"score": sim_score, "doc": doc})
            # Sort results by score in desc order
            results.sort(key=lambda k: k["score"], reverse=True)

        return result


with open(stopwords_file_path, "r") as fh:
    stopwords = fh.read().split(",")
    ds = DocSim(word2vec, stopwords=stopwords)


def short(source_answer, target_answer):
    sim_scores = ds.calculate_similarity(source_answer, target_answer)
    key_match = KeyWordmatching(source_answer, target_answer)
    key_Error = GrammerChecker(source_answer)

    marks1 = (
        ((sum(sim_scores) / len(sim_scores)) * 70) + (10 / key_match) + (20 * key_Error)
    )
    return marks1


# def essay(source_answer, target_answer):
#     sim_scores = ds.calculate_similarity(source_answer, target_answer)
#     key_match = KeyWordmatching(source_answer, target_answer)
#     key_Error = GrammerChecker(source_answer)
#     key_length = CheckLenght(source_answer)
#     marks2 = (
#         ((sum(sim_scores) / len(sim_scores)) * 60)
#         + (10 / key_match)
#         + (20 * key_Error)
#         + (10 / key_length)
#     )
#     return marks2
