from os import environ
from os.path import expanduser

HOME = expanduser('~')
reddit_secret = environ['REDDIT_SECRET']
client_id = environ['REDDIT_CLIENT_ID']
redirect_uri = "http://127.0.0.1:65010/authorize_callback"
POSTS_PER_MINUTE = 500  # This is way beyond my estimate but it worked for my test of 10 to 15 min

child_directories = [
    'fresh',
    'updated_1hr',
    'updated_2hr',
    'updated_3hr',
    'updated_4hr',
    'updated_5hr',
    'updated_6hr',
    'updated_7hr',
    'updated_8hr',
]


def next_dir(current):
    if current == child_directories[-1]:
        return None
    return child_directories[child_directories.index(current) + 1]
