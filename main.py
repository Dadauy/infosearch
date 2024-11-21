from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize
from nltk.corpus import stopwords
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from parsing_texts_animals import urls
import string
import re

nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('punkt_tab')

COUNT_TESTS = 2


def preprocess_text(text):
    text = text.lower()
    spec_chars = string.punctuation + '\n\xa0«»\t—…↑†'
    text = "".join([ch for ch in text if ch not in spec_chars])
    text = re.sub('\\d', '', text)
    tokens = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()
    clean_tokens = [lemmatizer.lemmatize(t) for t in tokens]
    stop_words = set(stopwords.words('russian'))
    filtered_tokens = [t for t in clean_tokens if not t in stop_words]
    return " ".join(filtered_tokens)


def open_text(idx, dir):
    text = ""
    with open(f"{dir}/{idx}.txt", encoding="utf-8") as file:
        for i in file.readlines():
            text += i
    text = preprocess_text(text)
    return text


train_texts = []  # список текстов для обучения
train_headers = []  # список заголовков для обучения

for idx in range(len(urls)):
    # if idx in [53]:
    #     continue
    title, text = open_text(idx, "Ytrain"), open_text(idx, "Xtrain")
    train_texts.append(text)
    train_headers.append(title)

# print(train_headers[0])
# print(train_texts[0])

vectorizer = TfidfVectorizer()
X_train = vectorizer.fit_transform(train_texts)
Y_train = train_headers

# Разделение данных на обучающую и тестовую выборки
# X_train, X_test, y_train, y_test = train_test_split(X_train, y_train, test_size=0.2, random_state=42)

clf = MultinomialNB(alpha=0.1, fit_prior=False)
clf.fit(X_train, Y_train)


def generate_headers():
    texts = []
    for idx in range(COUNT_TESTS):
        texts.append(open_text(idx, "tests"))
    new = vectorizer.transform(texts)
    return clf.predict(new)


headers = generate_headers()
print(headers)
