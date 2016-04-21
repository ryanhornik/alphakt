#!/usr/bin/env python3
import os

import praw
from candidate_identification import log_in_range
from candidate_update import update_submissions
from contants import child_directories, access_credentials, client_id, reddit_secret, redirect_uri, HOME


def main():
    reddit = praw.Reddit(user_agent="alpha_kt")
    reddit.set_oauth_app_info(client_id=client_id, client_secret=reddit_secret, redirect_uri=redirect_uri)
    reddit.set_access_credentials(**access_credentials)

    if not os.path.isdir(HOME):
        os.mkdir(HOME)
        for directory in child_directories:
            os.mkdir('{}/{}'.format(HOME, directory))

    for directory in child_directories:
        update_submissions(reddit, directory)
    log_in_range(reddit, start=0, end=60)  # Happens second so it won't get updated

if __name__ == "__main__":
    main()
