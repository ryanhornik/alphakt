#!/usr/bin/env python
import csv
import time

import praw
import os
import sys

HOME = os.path.expanduser('~')

POSTS_LOGGED = 0
reddit_secret = os.environ['REDDIT_SECRET']
client_id = os.environ['REDDIT_CLIENT_ID']
redirect_uri = "http://127.0.0.1:65010/authorize_callback"
POSTS_PER_MINUTE = 500  # This is way beyond my estimate but it worked for my test of 10 to 15 min

dataset = []


def log_post(submission):
    sub_dict = {
        "title": submission.title
    }
    dataset.append(sub_dict)


def save_dataset():
    if not os.path.isdir('{}/.alphakt'.format(HOME)):
        os.mkdir('{}/.alphakt'.format(HOME))
    with open('{}/.alphakt/{}.csv'.format(HOME, time.time()), 'w') as data_file:
        writer = csv.DictWriter(data_file, fieldnames=["title"])
        writer.writerows(dataset)
        data_file.close()


def log_in_range(start, end):
    all_submissions = r.get_subreddit('all').get_new(limit=POSTS_PER_MINUTE*(end - start))

    current_time = time.time()
    for submission in all_submissions:
        sub_age_minutes = (current_time - submission.created_utc) / 60
        if end > sub_age_minutes > start:
            log_post(submission)
        elif sub_age_minutes > end:
            break
    save_dataset()


if __name__ == "__main__":
    start = int(sys.argv[1]) if len(sys.argv) >= 3 else 10
    end = int(sys.argv[2]) if len(sys.argv) >= 3 else 15
    r = praw.Reddit(user_agent="alpha_kt")
    r.set_oauth_app_info(client_id=client_id, client_secret=reddit_secret, redirect_uri=redirect_uri)
    log_in_range(start=start, end=end)
