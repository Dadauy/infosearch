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
import numpy as np
from sklearn.decomposition import TruncatedSVD
from concurrent.futures import ProcessPoolExecutor

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


def open_text():
    pwd_file = "../tests/0.txt"
    text = ""
    with open(pwd_file, encoding='utf-8') as file:
        for i in file.readlines():
            text += i
    return text


def preprocess_text(text):
    text = text.lower()
    spec_chars = string.punctuation + '\n\xa0«»\t—…↑†'
    text = "".join([ch for ch in text if ch not in spec_chars])
    text = re.sub('\\d', '', text)
    tokens = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()
    clean_tokens = [lemmatizer.lemmatize(t) for t in tokens]
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [t for t in clean_tokens if not t in stop_words]
    return " ".join(filtered_tokens)


def minus_text(text):
    max_symbol = 4096
    sentences = [[t, 0, idx] for idx, t in enumerate(sent_tokenize(text))]
    text_word_tokenize = word_tokenize(preprocess_text(text))
    dct_word_point = dict()
    for word in text_word_tokenize:
        if word in dct_word_point:
            dct_word_point[word] += 1
        else:
            dct_word_point[word] = 1
    for idx in range(len(sentences)):
        for word in dct_word_point:
            sentences[idx][1] += dct_word_point[word] * sentences[idx][0].count(word)
        sentences[idx][1] /= len(preprocess_text(sentences[idx][0]).strip().split(" "))
    sentences.sort(key=lambda x: x[1])
    count = 0
    answer = []
    while sentences and (count + len(sentences[-1])) < max_symbol:
        sent = sentences.pop()
        count += len(sent[0])
        answer.append(sent)
    answer.sort(key=lambda x: x[2])
    text_answer = ""
    for sent in answer:
        text_answer += sent[0]
    return text_answer


def summarize():
    pipe = pipeline("summarization", model="facebook/bart-large-cnn")
    text = open_text()

    tokenize_text = sent_tokenize(text)
    text_en = thread_translate(tokenize_text, "ru", "en")
    text_en = minus_text(text_en)
    data_to_process = [[140, 100], [120, 80], [100, 60], [80, 40]]
    results = []
    for data in data_to_process:
        print(data)
        results.append(pipe(text_en, max_length=data[0], min_length=data[1], do_sample=True)[0]['summary_text'])
    print(results)
    result_text_en = " ".join(results)
    summary = pipe(result_text_en, max_length=120, min_length=80, do_sample=True)
    tokenize_text = sent_tokenize(summary[0]['summary_text'])
    text_ru = thread_translate(tokenize_text, "en", "ru")
    return text_ru


if __name__ == "__main__":
    print(summarize())

"""Первые признаки родовой деятельности у кошки однотипные и начинаются за 2-3 дня до важной даты. 
Кошка активно ищет укромное тихое место и проводит там много времени.
 Это признак того, что в скором времени в доме появятся новорожденные котята.
  Кошки обычно рожают вечером или ночью.
   Лучше всего родить 3-4 малышей – тогда меньше вероятность осложнений.
"""
