from __future__ import print_function
import time
import praw
import os

POSTS_LOGGED = 0
reddit_secret = os.environ['REDDIT_SECRET']
client_id = os.environ['REDDIT_CLIENT_ID']
redirect_uri = "http://127.0.0.1:65010/authorize_callback"
POSTS_PER_MINUTE = 500  # This is way beyond my estimate but it worked for my test of 10 to 15 min


def log_post(submission):
    pass  # some logic that add the post to the training set or testing set


def log_in_range(start, end):
    all_submissions = r.get_subreddit('all').get_new(limit=POSTS_PER_MINUTE*(end - start))

    current_time = time.time()
    for submission in all_submissions:
        sub_age_minutes = (current_time - submission.created_utc) / 60
        if end > sub_age_minutes > start:
            log_post(submission)
        elif sub_age_minutes > end:
            break


if __name__ == "__main__":
    r = praw.Reddit(user_agent="alpha_kt")
    r.set_oauth_app_info(client_id=client_id, client_secret=reddit_secret, redirect_uri=redirect_uri)
    log_in_range(start=10, end=15)
