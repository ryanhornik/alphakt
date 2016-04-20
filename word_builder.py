
import csv
import os
import re
import sys

ascii = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890'
redditWordsDict = {}
HOME = os.path.expanduser('~')

def save_dataset(path):
    if not os.path.isdir('{}/.alphakt'.format(HOME)):
        os.mkdir('{}/.alphakt'.format(HOME))
    with open(path[:-4] + "WordsCount" + path[-4:], 'w') as data_file:
        #fieldnames = ['Word', 'Count']
        writer = csv.writer(data_file)

        for row in redditWordsDict.items():
            writer.writerow(row)
        data_file.close()

def get_words(path):
    with open(path) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            putWords(cleanWords(row['title'].split()), 3)
            putWords(cleanWords(row['selftext'].split()), 1)

def putWords(words, weight):
    for word in words:
        redditWordsDict[word] = redditWordsDict.get(word, 0) + weight

def cleanWords(words):
    returnWords = []
    for word in words:
        returnWords.append(re.sub('[^0-9a-zA-Z]+', '', word.lower()))
    return returnWords

def main():
    path = sys.argv[1] if len(sys.argv) >= 2 else exit("Pass in file path")
    get_words(path)
    save_dataset(path)

if __name__ == "__main__":
    main()