import translators as ts
from nltk import sent_tokenize
import os
from concurrent.futures import ThreadPoolExecutor
from sklearn.feature_extraction.text import TfidfVectorizer
import string
import re
from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize
from nltk.corpus import stopwords
import nltk
from stop_words import get_stop_words
import numpy as np
from sklearn.decomposition import TruncatedSVD
from concurrent.futures import ProcessPoolExecutor
from nltk.stem import PorterStemmer

os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
from transformers import pipeline

nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('punkt_tab')


def task_function(param, one, two):
    result = ts.translate_text(param, from_language=one, to_language=two)
    return result


def thread_translate(params, one, two):
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(task_function, param, one, two) for param in params]

    results = [future.result() for future in futures]
    aggregated_result = " ".join(results)
    return aggregated_result


def open_text(pwd_file):
    text = ""
    with open(pwd_file, encoding='utf-8') as file:
        for i in file.readlines():
            text += i
    return text


def preprocess_text_more_stopwords(text):
    text = text.lower()
    spec_chars = string.punctuation + '\n\xa0«»\t—…↑†'
    text = "".join([ch for ch in text if ch not in spec_chars])
    text = re.sub('\\d', '', text)
    tokens = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()
    clean_tokens = [lemmatizer.lemmatize(t) for t in tokens]
    stop_words_3 = [i.replace("\n", "") for i in open_text("../stopwords.txt").split("\n")]
    stop_words = set(stopwords.words('english') + get_stop_words('english') + stop_words_3)
    # print(stop_words)
    filtered_tokens = [t for t in clean_tokens if not t in stop_words]
    return " ".join(filtered_tokens)


def preprocess_text(text):
    text = text.lower()
    spec_chars = string.punctuation + '\n\xa0«»\t—…↑†'
    text = "".join([ch for ch in text if ch not in spec_chars])
    text = re.sub('\\d', '', text)
    tokens = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()
    clean_tokens = [lemmatizer.lemmatize(t) for t in tokens]
    stop_words = set(stopwords.words('english'))
    # print(stop_words)
    filtered_tokens = [t for t in clean_tokens if not t in stop_words]
    return " ".join(filtered_tokens)


def minus_text(text):
    text_word_tokenize = word_tokenize(preprocess_text_more_stopwords(text))
    dct_word_point = dict()
    for word in text_word_tokenize:
        if word in dct_word_point:
            dct_word_point[word] += 1
        else:
            dct_word_point[word] = 1
    a = [[dct_word_point[i], i] for i in dct_word_point]
    a.sort()
    a.reverse()
    # print(a)
    return a[0:4]


def key_word_text(key_words, text_en):
    text_word_tokenize = sent_tokenize(text_en)
    lst_key_word_sent = [[] for idx in range(len(key_words))]
    for idx in range(len(key_words)):
        for sent in text_word_tokenize:
            if key_words[idx] in sent:
                lst_key_word_sent[idx].append(sent)
    # print(lst_key_word_sent)
    # print(key_words)
    lst = [key_words[0]]
    lst_1 = [lst_key_word_sent[0]]
    for idx in range(len(key_words) - 1):
        if lst_key_word_sent[idx] == lst_key_word_sent[idx + 1]:
            lst[-1] += " " + key_words[idx + 1]
        else:
            lst.append(key_words[idx + 1])
            lst_1.append(lst_key_word_sent[idx + 1].copy())
    return lst, lst_1


def key_word():
    pipe = pipeline("summarization", model="facebook/bart-large-cnn")
    text = open_text("../tests/0.txt")

    tokenize_text = sent_tokenize(text)
    text_en = thread_translate(tokenize_text, "ru", "en")
    key = [i[1] for i in minus_text(text_en)]
    key, sent = key_word_text(key, text_en)
    answer = []
    for idx in range(len(key)):
        text_en = " ".join(sent[idx])
        summary = pipe(text_en, max_length=15, min_length=5, do_sample=False)[0]['summary_text']
        answer_en = key[idx] + " - " + summary
        text_ru = ts.translate_text(answer_en, from_language="en", to_language="ru")
        answer.append(text_ru)
    return answer


if __name__ == "__main__":
    for i in key_word():
        print(i)

"""
кошка – первые признаки родовой деятельности у кошки бывают двух типов.
котенок - первый котенок появляется на свет в течение 2 часов с момента рождения.
рождение - кошки обычно рожают вечером или ночью.
беременность - Существуют специальные калькуляторы беременности для определения вероятной даты наступления беременности.
"""
