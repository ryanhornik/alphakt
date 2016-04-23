#!/usr/bin/env python
import codecs
import csv
import praw
import os

from candidate_identification import log_post

from constants import HOME, reddit_secret, client_id, redirect_uri, child_directories, next_dir


updated_files = []


def save_dataset(directory, file_, dataset):
    with open("{}/{}/{}".format(HOME, next_dir(directory), file_), 'w') as data_file:
        fieldnames = list(next(iter(dataset.values())).keys())
        writer = csv.DictWriter(data_file, fieldnames=fieldnames)
        writer.writeheader()
        for key, value in dataset.items():
            writer.writerow(value)
        data_file.close()

    os.remove("{}/{}/{}".format(HOME, directory, file_))


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

    for file_ in os.listdir("{}/{}".format(HOME, directory)):
        if file_ in updated_files:
            continue
        path = "{}/{}/{}".format(HOME, directory, file_)

        dataset = dataset_from_file(path)
        ids = ["t3_" + key for key in dataset.keys()]

        updated_submissions = reddit.get_submissions(ids)
        for sub in updated_submissions:
            if sub is not None:
                next_directory = next_dir(directory)
                dataset[sub.id][next_directory + "_score"] = sub.score
                dataset[sub.id][next_directory + "_ups"] = sub.ups
                dataset[sub.id][next_directory + "_downs"] = sub.downs
                dataset[sub.id][next_directory + "_num_comments"] = sub.num_comments
                dataset[sub.id][next_directory + "_gilded"] = sub.gilded
                dataset[sub.id][next_directory + "_num_reports"] = sub.num_reports or 0
                dataset[sub.id][next_directory + "_locked"] = sub.locked
                dataset[sub.id][next_directory + "_edited"] = True if sub.edited is not False else False
        save_dataset(directory, file_, dataset)

        updated_files.append(file_)


def main():
    reddit = praw.Reddit(user_agent="alpha_kt")
    reddit.set_oauth_app_info(client_id=client_id, client_secret=reddit_secret, redirect_uri=redirect_uri)
    for directory in child_directories:
        update_submissions(reddit, directory)


if __name__ == "__main__":
    main()
