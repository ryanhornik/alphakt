#!/usr/bin/env python
import csv
import os
import re

from constants import HOME


def save_dataset(path, word_counts):
    if not os.path.isdir(HOME):
        os.mkdir(HOME)

    with open(path[:-4] + "WordsCount" + path[-4:], 'w') as data_file:
        writer = csv.writer(data_file)

        for row in word_counts.items():
            writer.writerow(row)
        data_file.close()


def get_words(path, word_counts):
    csvfile = open(path)
    reader = csv.DictReader(csvfile)
    for row in reader:
        for word in clean_words(row['title'].lower().split()):
            word_counts[word] = word_counts.get(word, 0) + 3
        for word in clean_words(row['selftext'].lower().split()):
            word_counts[word] = word_counts.get(word, 0) + 1


def clean_words(words):
    alphanumeric = re.compile(r'[^0-9a-z]+')
    return filter(None, map(lambda word: alphanumeric.sub('', word), words))


def main(path):
    word_counts = {}
    get_words(path, word_counts)
    save_dataset(path, word_counts)


def prune(path):
    file = open(path)
    outfile = open(path[:-4] + "_pruned" + path[-4:], mode='w')
    reader = csv.reader(file)
    writer = csv.writer(outfile)

    for row in reader:
        if int(row[1]) < 500 or len(row[0]) <= 3 or int(row[1]) > 6000:
            continue
        writer.writerow(row)


def split(path, n):
    file = open(path)
    outfiles = [open(path[:-4] + "_split_" + str(x) + path[-4:], mode='w') for x in range(1, n + 1)]
    reader = csv.reader(file)
    writers = [csv.writer(f) for f in outfiles]

    for i, row in enumerate(reader):
        writers[i % n].writerow(row)


if __name__ == "__main__":
    from sys import argv

    if len(argv) >= 2:
        main(argv[1])
    else:
        exit("Pass in file path")
