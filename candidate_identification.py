#!/usr/bin/env python
import csv
import os
import time
from datetime import datetime

import praw

from contants import HOME, client_id, reddit_secret, redirect_uri, POSTS_PER_MINUTE, child_directories

POSTS_LOGGED = 0


def log_post(submission):
    created_time = datetime.fromtimestamp(submission.created_utc)
    sub_dict = {
        "quarantine": submission.quarantine,
        "_timeStamp": submission.created_utc,
        "domain": "self" if submission.is_self else submission.domain,
        "hidden": submission.hidden,
        "removal_reason": submission.removal_reason,
        "selftext": submission.selftext,
        "id": submission.id,
        "author": submission.author,
        "num_reports": submission.num_reports or 0,
        "stickied": submission.stickied,
        "gilded": submission.gilded,
        "created_seconds_since_midnight":
            (created_time - created_time.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds(),
        "created_day_of_week": created_time.weekday(),
        "is_self": submission.is_self,
        "author_flair_text": submission.author_flair_text,
        "ups": submission.ups,
        "score": submission.score,
        "subreddit": submission.subreddit,
        "over_18": submission.over_18,
        "title": submission.title,
        "downs": submission.downs,
        "locked": submission.locked,
        "distinguished": submission.distinguished,
        "num_comments": submission.num_comments,
        "edited": True if submission.edited is not False else False,  # submission.edited is either False or int.
        "link_flair_text": submission.link_flair_text,
    }
    return sub_dict


def save_dataset(dataset):
    if not os.path.isdir('{}/.alphakt'.format(HOME)):
        os.mkdir('{}/.alphakt'.format(HOME))
        for directory in child_directories:
            os.mkdir('{}/.alphakt/{}'.format(HOME, directory))
    with open('{}/.alphakt/fresh/{}.csv'.format(HOME, time.time()), 'w') as data_file:
        fieldnames = list(dataset[0].keys())
        writer = csv.DictWriter(data_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(dataset)
        data_file.close()


def log_in_range(reddit, start, end):
    all_submissions = reddit.get_subreddit('all').get_new(limit=POSTS_PER_MINUTE * end)
    dataset = []

    current_time = time.time()
    for submission in all_submissions:
        sub_age_minutes = (current_time - submission.created_utc) / 60
        if end > sub_age_minutes > start:
            dataset.append(log_post(submission))
        elif sub_age_minutes > end:
            break
    save_dataset(dataset)


def main(start, end):
    reddit = praw.Reddit(user_agent="alpha_kt")
    reddit.set_oauth_app_info(client_id=client_id, client_secret=reddit_secret, redirect_uri=redirect_uri)
    log_in_range(reddit, start=start, end=end)


if __name__ == "__main__":
    from sys import argv
    main(start=int(argv[1]) if len(argv) >= 3 else 0,
         end=int(argv[2]) if len(argv) >= 3 else 60)
