#!/usr/bin/env python
import csv
import praw
import os

from candidate_identification import log_post

from contants import HOME, reddit_secret, client_id, redirect_uri


dataset = []
submissionIds = []


def save_dataset(path):
    if not os.path.isdir('{}/.alphakt'.format(HOME)):
        os.mkdir('{}/.alphakt'.format(HOME))
    with open(path[:-4] + "Updated" + path[-4:], 'w') as data_file:
        fieldnames = list(dataset[0].keys())
        writer = csv.DictWriter(data_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(dataset)
        data_file.close()


def get_submission_ids(path):
    with open(path) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            submissionIds.append('t3_' + row['id'])
            print('Adding submission ID ' + row['id'])


def update_submissions(reddit, path):
    get_submission_ids(path)

    updated_submissions = reddit.get_submissions(submissionIds)
    for sub in updated_submissions:
        if sub is not None:
            log_post(sub)
    save_dataset(path)


def main(path):
    reddit = praw.Reddit(user_agent="alpha_kt")
    reddit.set_oauth_app_info(client_id=client_id, client_secret=reddit_secret, redirect_uri=redirect_uri)
    update_submissions(reddit, path)


if __name__ == "__main__":
    from sys import argv
    main(argv[1] if len(argv) >= 2 else exit("Pass in file path"))
