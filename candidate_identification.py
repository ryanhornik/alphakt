import praw
import os
from pprint import pprint

reddit_secret = os.environ['REDDIT_SECRET']
client_id = os.environ['REDDIT_CLIENT_ID']
redirect_uri = "http://127.0.0.1:65010/authorize_callback"

if __name__ == "__main__":
    r = praw.Reddit(user_agent="alpha_kt")
    r.set_oauth_app_info(client_id=client_id, client_secret=reddit_secret, redirect_uri=redirect_uri)
    new_posts = r.get_subreddit('all').get_new(limit=10)

    for s in new_posts:
        pprint(vars(s))
        break

