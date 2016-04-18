#!/usr/bin/env python

import csv
import time
from datetime import datetime

import praw
import os
import sys

HOME = os.path.expanduser('~')
reddit_secret = os.environ['REDDIT_SECRET']
client_id = os.environ['REDDIT_CLIENT_ID']
redirect_uri = "http://127.0.0.1:65010/authorize_callback"

dataset = []
submissionIds=[]

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
    dataset.append(sub_dict)



def save_dataset(path):
    if not os.path.isdir('{}/.alphakt'.format(HOME)):
        os.mkdir('{}/.alphakt'.format(HOME))
    with open(path[:-4] + "Updated" + path[-4:], 'w') as data_file:
        fieldnames = list(dataset[0].keys())
        writer = csv.DictWriter(data_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(dataset)
        data_file.close()

def get_submissionIDs(path):
    with open(path) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            submissionIds.append('t3_' + row['id'])
            print('Adding submission ID ' + row['id'])


def update_submissions(reddit, path):
    get_submissionIDs(path)

    updated_submissions = reddit.get_submissions(submissionIds)
    for sub in updated_submissions:
        if sub is not None:
            log_post(sub)
    save_dataset(path)


def main():
    path = sys.argv[1] if len(sys.argv) >= 2 else exit("Pass in file path")
    reddit = praw.Reddit(user_agent="alpha_kt")
    reddit.set_oauth_app_info(client_id=client_id, client_secret=reddit_secret, redirect_uri=redirect_uri)
    update_submissions(reddit, path)


if __name__ == "__main__":
    main()