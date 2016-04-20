#!/usr/bin/env python
import csv
import os
import re

HOME = os.path.expanduser('~')


def save_dataset(path, word_counts):
    if not os.path.isdir('{}/.alphakt'.format(HOME)):
        os.mkdir('{}/.alphakt'.format(HOME))

    with open(path[:-4] + "WordsCount" + path[-4:], 'w') as data_file:
        writer = csv.writer(data_file)

        for row in word_counts.items():
            writer.writerow(row)
        data_file.close()


def get_words(path, word_counts):
    with open(path) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            put_words(clean_words(row['title'].split()), 3, word_counts)
            put_words(clean_words(row['selftext'].split()), 1, word_counts)


def put_words(words, weight, word_counts):
    for word in words:
        word_counts[word] = word_counts.get(word, 0) + weight


def clean_words(words):
    alphanumeric = re.compile(r'[^0-9a-z]+')
    return map(lambda word: alphanumeric.sub('', word), words)


def main(path):
    word_counts = {}
    get_words(path, word_counts)
    save_dataset(path, word_counts)


if __name__ == "__main__":
    from sys import argv
    if len(argv) >= 2:
        main(argv[1])
    else:
        exit("Pass in file path")
