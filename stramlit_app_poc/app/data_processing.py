import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
import string
import numpy as np
from gensim.models import Word2Vec
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import gensim.downloader as api
import re
import pdfplumber
from gensim.models.fasttext import FastText as FT_gensim


def tokeniser(texte):
    words = word_tokenize(texte)
    stemmer_en = SnowballStemmer("english")
    stemmer_fr = SnowballStemmer("french")
    stopwords_fr_en = stopwords.words("english") + stopwords.words("french")
    words = [
        word
        for word in words
        if word.lower() not in stopwords_fr_en and word not in string.punctuation
    ]
    stemmed_words = [stemmer_fr.stem(word) for word in words] + [
        stemmer_en.stem(word) for word in words
    ]
    return set(stemmed_words)


def appliquer_tokenisation_et_filtrage(texte, competences_tokenized_flat):
    tokens = tokeniser(texte)
    return [token for token in tokens if token in competences_tokenized_flat]


def preparer_liste_competences(liste_competences):
    return {
        item for sublist in liste_competences for item in tokeniser(" ".join(sublist))
    }


def filtrer_competences_df(df, liste_competences):
    competences_tokenized_flat = preparer_liste_competences(liste_competences)
    df["competence_processed"] = df["description"].apply(
        lambda x: appliquer_tokenisation_et_filtrage(x, competences_tokenized_flat)
    )
    return df


def filtrer_competences_texte(texte, liste_competences):
    competences_tokenized_flat = preparer_liste_competences(liste_competences)
    return appliquer_tokenisation_et_filtrage(texte, competences_tokenized_flat)


def lirePDF(chemin_acces):
    # Extraire le texte du PDF
    with pdfplumber.open(chemin_acces) as pdf:
        texte = ""
        for page in pdf.pages:
            texte += page.extract_text()

    texte = re.sub(r"http\S+", " ", texte)  # enlever liens(texte)

    texte = re.sub(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", " ", texte
    )  # enlever adresses email

    texte = re.sub(r"[0-9()+-]", " ", texte)  # enlever numeros et symboles

    texte = re.sub(r"[^\w\s]", " ", texte)  # enlever symboles

    return texte


def liretexte(texte):
    texte = re.sub(r"http\S+", " ", texte)  # enlever liens(texte)

    texte = re.sub(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", " ", texte
    )  # enlever adresses email

    texte = re.sub(r"[0-9()+-]", " ", texte)  # enlever numeros et symboles

    texte = re.sub(r"[^\w\s]", " ", texte)  # enlever symboles

    return texte
