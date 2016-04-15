#!/usr/bin/env python
import csv
import time
from datetime import datetime

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
    created_time = datetime.fromtimestamp(submission.created_utc)
    sub_dict = {
        "quarantine": submission.quarantine,
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
    dataset.append(sub_dict)


def save_dataset():
    if not os.path.isdir('{}/.alphakt'.format(HOME)):
        os.mkdir('{}/.alphakt'.format(HOME))
    with open('{}/.alphakt/{}.csv'.format(HOME, time.time()), 'w') as data_file:
        fieldnames = list(dataset[0].keys())
        writer = csv.DictWriter(data_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(dataset)
        data_file.close()


def log_in_range(reddit, start, end):
    all_submissions = reddit.get_subreddit('all').get_new(limit=POSTS_PER_MINUTE * end)

    current_time = time.time()
    for submission in all_submissions:
        sub_age_minutes = (current_time - submission.created_utc) / 60
        if end > sub_age_minutes > start:
            log_post(submission)
        elif sub_age_minutes > end:
            break
    save_dataset()


def main():
    start = int(sys.argv[1]) if len(sys.argv) >= 3 else 0
    end = int(sys.argv[2]) if len(sys.argv) >= 3 else 5
    reddit = praw.Reddit(user_agent="alpha_kt")
    reddit.set_oauth_app_info(client_id=client_id, client_secret=reddit_secret, redirect_uri=redirect_uri)
    log_in_range(reddit, start=start, end=end)


if __name__ == "__main__":
    main()
