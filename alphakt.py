#!/usr/bin/env python3
import praw
from candidate_identification import log_in_range
from candidate_update import update_submissions
from contants import client_id, reddit_secret, redirect_uri, child_directories


def main():
    reddit = praw.Reddit(user_agent="alpha_kt")
    reddit.set_oauth_app_info(client_id=client_id, client_secret=reddit_secret, redirect_uri=redirect_uri)
    log_in_range(reddit, start=0, end=60)
    for directory in child_directories:
        update_submissions(reddit, directory)

if __name__ == "__main__":
    main()
