from os import environ
from os.path import expanduser

HOME = expanduser('~/.alphakt')
reddit_secret = environ['REDDIT_SECRET']
client_id = environ['REDDIT_CLIENT_ID']
redirect_uri = "http://127.0.0.1:65010/authorize_callback"
POSTS_PER_MINUTE = 500  # This is way beyond my estimate but it worked for my test of 10 to 15 min

access_credentials = {
    'access_token': environ['ACCESS_TOKEN'],
    'refresh_token': environ['REFRESH_TOKEN'],
    'scope': {'read'}
}


child_directories = [
    'fresh',
    '1hr', '2hr', '3hr', '4hr',
    '5hr', '6hr', '7hr', '8hr',
]


def next_dir(current):
    if current == child_directories[-1]:
        return None
    return child_directories[child_directories.index(current) + 1]
