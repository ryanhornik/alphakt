#!/usr/bin/env python
import codecs
import csv
import praw
import os

from candidate_identification import log_post

from contants import HOME, reddit_secret, client_id, redirect_uri, child_directories, next_dir


updated_files = []


def save_dataset(directory, file_, dataset):
    with open("{}/.alphakt/{}/{}".format(HOME, next_dir(directory), file_), 'w') as data_file:
        fieldnames = list(next(iter(dataset.values())).keys())
        writer = csv.DictWriter(data_file, fieldnames=fieldnames)
        writer.writeheader()
        for key, value in dataset.items():
            writer.writerow(value)
        data_file.close()

    os.remove("{}/.alphakt/{}/{}".format(HOME, directory, file_))


def dataset_from_file(path):
    dataset = {}
    with open(path) as csvfile:
        reader = csv.DictReader(x.replace('\0', '') for x in csvfile)
        for row in reader:
            dataset[row['id']] = row
    return dataset


def update_submissions(reddit, directory):
    if directory == child_directories[-1]:
        return

    for file_ in os.listdir("{}/.alphakt/{}".format(HOME, directory)):
        if file_ in updated_files:
            continue
        path = "{}/.alphakt/{}/{}".format(HOME, directory, file_)

        dataset = dataset_from_file(path)
        ids = ["t3_" + key for key in dataset.keys()]

        updated_submissions = reddit.get_submissions(ids)
        for sub in updated_submissions:
            if sub is not None:
                dataset[sub.id][next_dir(directory)] = sub.score
        save_dataset(directory, file_, dataset)

        updated_files.append(file_)


def main():
    reddit = praw.Reddit(user_agent="alpha_kt")
    reddit.set_oauth_app_info(client_id=client_id, client_secret=reddit_secret, redirect_uri=redirect_uri)
    for directory in child_directories:
        update_submissions(reddit, directory)


if __name__ == "__main__":
    main()
