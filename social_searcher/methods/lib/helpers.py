import codecs
import pymorphy2
from os import path
import re
from collections import Counter


morph = pymorphy2.MorphAnalyzer()
files_dir = path.join(path.dirname(__file__), 'files')

with codecs.open(path.join(files_dir, 'stop_words.txt'), 'r', 'utf-8') as f:
    stop_words = f.read()
    stop_words = stop_words.split()


def filter_words(words):
    for w in words:
        w = w.group()
        w = morph.parse(w.lower())[0]

        # записываем только существительные, потому что они более информативны
        if w.normal_form in stop_words or 'NOUN' not in w.tag:
            continue

        yield w.normal_form


# функция, добавляющая слова из текста к рейтингу
def count_words(text):
    pattern = re.compile(r'\b[^\W\d]+\b')
    words = pattern.finditer(text)

    return Counter(filter_words(words))


def word_rate(collection):
    rate = Counter()

    # считаем количество входений слов в документ
    for doc in collection:
        words = count_words(doc)
        total_words = sum(words.values())

        for w in words:
            words[w] /= total_words

        rate.update(words)

    return rate.most_common(100)
